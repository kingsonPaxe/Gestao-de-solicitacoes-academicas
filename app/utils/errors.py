from flask import render_template


def register_error_handlers(app):
    @app.errorhandler(403)
    def forbidden(e):
        return render_template("error.html", code=403,
                               message="Você não tem permissão para acessar esta página."), 403

    @app.errorhandler(404)
    def not_found(e):
        return render_template("error.html", code=404,
                               message="Página não encontrada."), 404

    @app.errorhandler(413)
    def too_large(e):
        return render_template("error.html", code=413,
                               message="Arquivo muito grande."), 413

    @app.errorhandler(500)
    def server_error(e):
        return render_template("error.html", code=500,
                               message="Erro interno do servidor."), 500
