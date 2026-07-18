from ..database import db
from ..models import Usuario, TipoSolicitacao

TIPOS_PADRAO = [
    ("Declaração de Frequência", "Comprova a frequência do aluno no curso."),
    ("Histórico Escolar", "Emissão de histórico escolar oficial."),
    ("Revisão de Nota", "Pedido de revisão de avaliação."),
    ("Mudança de Curso", "Solicitação de transferência entre cursos."),
    ("Trancamento de Matrícula", "Suspensão temporária da matrícula."),
    ("Segunda Via do Cartão", "Emissão de nova via do cartão estudantil."),
    ("Declaração de Conclusão", "Comprova a conclusão do curso."),
    ("Outros", "Outras solicitações."),
]

ALUNOS_DEMO = [
    ("Ana Silva", "Engenharia Informática"),
    ("Bruno Costa", "Direito"),
    ("Carla Mendes", "Economia"),
    ("Daniel Rocha", "Engenharia Civil"),
    ("Elisa Fernandes", "Medicina"),
    ("Fábio Lima", "Arquitetura"),
    ("Gabriela Souza", "Psicologia"),
    ("Hugo Almeida", "Contabilidade"),
    ("Inês Pereira", "Enfermagem"),
    ("João Neto", "Engenharia Eletrotécnica"),
]


def run_seed():
    # Admin
    if not Usuario.query.filter_by(email="admin@imetro.ao").first():
        admin = Usuario(nome="Administrador", email="admin@imetro.ao", tipo="admin")
        admin.set_password("123456")
        db.session.add(admin)

    # Tipos
    for nome, desc in TIPOS_PADRAO:
        if not TipoSolicitacao.query.filter_by(nome=nome).first():
            db.session.add(TipoSolicitacao(nome=nome, descricao=desc))

    # Alunos
    for i, (nome, curso) in enumerate(ALUNOS_DEMO, start=1):
        email = f"aluno{i}@imetro.ao"
        if not Usuario.query.filter_by(email=email).first():
            u = Usuario(nome=nome, email=email, curso=curso, tipo="aluno")
            u.set_password("123456")
            db.session.add(u)

    db.session.commit()
