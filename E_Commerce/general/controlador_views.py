from django.views import View


class GeneralView(View):
    def get(self, request, id_elemento=None):
        if request.path_info.endswith("index"):
            return self.index(request)
        elif request.path_info.endswith("registro"):
            return self.registro(request)
        elif request.path_info.endswith("ver"):
            return self.ver(request, id_elemento)
        elif request.path_info.endswith("eliminar") and id_elemento:
            return self.eliminar(request, id_elemento)

    def post(self, request, id_elemento=None):
        if request.path_info.endswith("registrar"):
            return self.registrar(request)
        elif request.path_info.endswith("editar") and id_elemento:
            return self.editar(request, id_elemento)
