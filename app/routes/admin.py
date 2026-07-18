from flask import Blueprint, render_template, redirect, url_for, flash, request, \
    send_from_directory, current_app, abort
from flask_login import login_required, current_user
from ..utils.decorators import admin_required
from ..forms.solicitacao_forms import AtualizarStatusForm
from ..forms.admin_forms import AlunoForm, TipoForm
from ..services.solicitacao_service import SolicitacaoService
from ..services.user_service import UserService
from ..services.tipo_service import TipoService
from ..repositories.solicitacao_repo import SolicitacaoRepository
from ..repositories.tipo_repo import TipoRepository
from ..repositories.user_repo import UserRepository
from ..models import StatusSolicitacao

admin_bp = Blueprint("admin", __name__)


@admin_bp.before_request
@login_required
@admin_required
def _guard():
    pass


@admin_bp.route("/dashboard")
def dashboard():
    stats = {
        "total": SolicitacaoRepository.count(),
        "alunos": UserRepository.count_alunos(),
        "pendentes": SolicitacaoRepository.count_in(StatusSolicitacao.PENDENTES),
        "concluidas": SolicitacaoRepository.count_in(StatusSolicitacao.FINALIZADAS),
    }
    por_status = SolicitacaoRepository.group_by_status()
    por_tipo = SolicitacaoRepository.group_by_tipo()
    ultimas = SolicitacaoRepository.latest(8)
    return render_template("dashboard_admin.html", stats=stats,
                           por_status=por_status, por_tipo=por_tipo,
                           ultimas=ultimas, statuses=StatusSolicitacao.ALL)


@admin_bp.route("/solicitacoes")
def listar():
    status = request.args.get("status") or None
    q = request.args.get("q") or None
    tipo_id = request.args.get("tipo_id", type=int) or None
    itens = SolicitacaoRepository.all(status=status, search_aluno=q, tipo_id=tipo_id)
    return render_template("listar_solicitacoes.html", itens=itens,
                           status_atual=status, search=q,
                           statuses=StatusSolicitacao.ALL, is_admin=True,
                           tipos=TipoRepository.all(), tipo_atual=tipo_id)


@admin_bp.route("/solicitacoes/<int:sid>", methods=["GET", "POST"])
def detalhes(sid):
    s = SolicitacaoRepository.get(sid)
    if not s:
        abort(404)
    form = AtualizarStatusForm()
    form.status.choices = [(x, x) for x in StatusSolicitacao.ALL]
    if request.method == "GET":
        form.status.data = s.status
    if form.validate_on_submit():
        try:
            SolicitacaoService.atualizar_status(
                sid, form.status.data, form.observacao.data,
                current_user.nome, arquivo=form.arquivo.data,
            )
            flash("Solicitação atualizada.", "success")
            return redirect(url_for("admin.detalhes", sid=sid))
        except ValueError as e:
            flash(str(e), "danger")
    return render_template("detalhes.html", s=s, is_admin=True, form=form)


@admin_bp.route("/solicitacoes/<int:sid>/excluir", methods=["POST"])
def excluir_solicitacao(sid):
    try:
        SolicitacaoService.excluir(sid)
        flash("Solicitação excluída.", "success")
    except ValueError as e:
        flash(str(e), "danger")
    return redirect(url_for("admin.listar"))


@admin_bp.route("/solicitacoes/<int:sid>/download")
def download(sid):
    s = SolicitacaoRepository.get(sid)
    if not s or not s.arquivo:
        abort(404)
    return send_from_directory(current_app.config["UPLOAD_FOLDER"],
                               s.arquivo, as_attachment=True)


# ---- Alunos ----
@admin_bp.route("/alunos")
def alunos():
    q = request.args.get("q") or None
    itens = UserRepository.list_alunos(search=q)
    return render_template("admin_alunos.html", itens=itens, search=q)


@admin_bp.route("/alunos/novo", methods=["GET", "POST"])
def novo_aluno():
    form = AlunoForm()
    if form.validate_on_submit():
        if not form.senha.data:
            flash("Informe uma senha inicial.", "danger")
        else:
            try:
                UserService.criar_aluno(form.nome.data, form.email.data,
                                        form.senha.data, form.curso.data)
                flash("Aluno cadastrado.", "success")
                return redirect(url_for("admin.alunos"))
            except ValueError as e:
                flash(str(e), "danger")
    return render_template("admin_aluno_form.html", form=form, editar=False)


@admin_bp.route("/alunos/<int:uid>/editar", methods=["GET", "POST"])
def editar_aluno(uid):
    u = UserRepository.get(uid)
    if not u or u.is_admin:
        abort(404)
    form = AlunoForm(obj=u)
    if form.validate_on_submit():
        try:
            UserService.atualizar_aluno(uid, form.nome.data, form.email.data,
                                        form.curso.data, form.senha.data or None)
            flash("Aluno atualizado.", "success")
            return redirect(url_for("admin.alunos"))
        except ValueError as e:
            flash(str(e), "danger")
    return render_template("admin_aluno_form.html", form=form, editar=True, uid=uid)


@admin_bp.route("/alunos/<int:uid>/excluir", methods=["POST"])
def excluir_aluno(uid):
    try:
        UserService.excluir_aluno(uid)
        flash("Aluno excluído.", "success")
    except ValueError as e:
        flash(str(e), "danger")
    return redirect(url_for("admin.alunos"))


# ---- Tipos ----
@admin_bp.route("/tipos", methods=["GET", "POST"])
def tipos():
    form = TipoForm()
    if form.validate_on_submit():
        try:
            TipoService.criar(form.nome.data, form.descricao.data)
            flash("Tipo cadastrado.", "success")
            return redirect(url_for("admin.tipos"))
        except ValueError as e:
            flash(str(e), "danger")
    return render_template("admin_tipos.html", form=form, itens=TipoRepository.all())


@admin_bp.route("/tipos/<int:tid>/excluir", methods=["POST"])
def excluir_tipo(tid):
    try:
        TipoService.excluir(tid)
        flash("Tipo excluído.", "success")
    except ValueError as e:
        flash(str(e), "danger")
    return redirect(url_for("admin.tipos"))
