from flask import Blueprint, render_template, redirect, url_for, flash, request, \
    send_from_directory, current_app, abort
from flask_login import login_required, current_user
from ..utils.decorators import aluno_required
from ..forms.solicitacao_forms import SolicitacaoForm
from ..services.solicitacao_service import SolicitacaoService
from ..repositories.solicitacao_repo import SolicitacaoRepository
from ..repositories.tipo_repo import TipoRepository
from ..models import StatusSolicitacao

aluno_bp = Blueprint("aluno", __name__)


@aluno_bp.before_request
@login_required
@aluno_required
def _guard():
    pass


@aluno_bp.route("/dashboard")
def dashboard():
    uid = current_user.id
    stats = {
        "total": SolicitacaoRepository.count_by_user(uid),
        "pendentes": SolicitacaoRepository.count_by_user_in(uid, StatusSolicitacao.PENDENTES),
        "em_analise": SolicitacaoRepository.count_by_user(uid, StatusSolicitacao.EM_ANALISE),
        "concluidas": SolicitacaoRepository.count_by_user_in(uid, StatusSolicitacao.FINALIZADAS),
    }
    ultimas = SolicitacaoRepository.latest(5, user_id=uid)
    return render_template("dashboard_aluno.html", stats=stats, ultimas=ultimas)


@aluno_bp.route("/solicitacoes")
def listar():
    status = request.args.get("status") or None
    search = request.args.get("q") or None
    itens = SolicitacaoRepository.by_user(current_user.id, status=status, search=search)
    return render_template("listar_solicitacoes.html", itens=itens,
                           status_atual=status, search=search,
                           statuses=StatusSolicitacao.ALL, is_admin=False)


@aluno_bp.route("/solicitacoes/nova", methods=["GET", "POST"])
def nova():
    form = SolicitacaoForm()
    form.tipo_id.choices = [(t.id, t.nome) for t in TipoRepository.all()]
    if form.validate_on_submit():
        SolicitacaoService.criar(current_user.id, form.tipo_id.data,
                                 form.descricao.data, current_user.nome)
        flash("Solicitação enviada com sucesso.", "success")
        return redirect(url_for("aluno.listar"))
    return render_template("nova_solicitacao.html", form=form, editar=False)


@aluno_bp.route("/solicitacoes/<int:sid>/editar", methods=["GET", "POST"])
def editar(sid):
    s = SolicitacaoService.get_para_aluno(sid, current_user.id)
    if not s:
        abort(404)
    if s.status != StatusSolicitacao.RECEBIDA:
        flash("Solicitação não pode mais ser editada.", "warning")
        return redirect(url_for("aluno.detalhes", sid=sid))
    form = SolicitacaoForm(obj=s)
    form.tipo_id.choices = [(t.id, t.nome) for t in TipoRepository.all()]
    if request.method == "GET":
        form.tipo_id.data = s.tipo_id
    if form.validate_on_submit():
        try:
            SolicitacaoService.editar_pelo_aluno(sid, current_user.id,
                                                 form.tipo_id.data, form.descricao.data)
            flash("Solicitação atualizada.", "success")
            return redirect(url_for("aluno.detalhes", sid=sid))
        except ValueError as e:
            flash(str(e), "danger")
    return render_template("nova_solicitacao.html", form=form, editar=True, sid=sid)


@aluno_bp.route("/solicitacoes/<int:sid>")
def detalhes(sid):
    s = SolicitacaoService.get_para_aluno(sid, current_user.id)
    if not s:
        abort(404)
    return render_template("detalhes.html", s=s, is_admin=False)


@aluno_bp.route("/solicitacoes/<int:sid>/download")
def download(sid):
    s = SolicitacaoService.get_para_aluno(sid, current_user.id)
    if not s or not s.arquivo:
        abort(404)
    return send_from_directory(current_app.config["UPLOAD_FOLDER"],
                               s.arquivo, as_attachment=True)
