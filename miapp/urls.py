from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    #MAIZ
    url(r'^analisis/$', views.analisisPagina, name='analisisPagina'),
    url(r'^agregar/$', views.nuevoEnfermedadPagina, name='nuevoEnfermedadPagina'),
    url(r'^api/reviews$', views.procesarCalificacion, name='procesarCalificacion'),
    url(r'^api/enfermedades$', views.crearEnfermedad, name='crearEnfermedad'),
    url(r'^api/analisis$', views.agregarAnalisis, name='agregarAnalisis'),
    url(r'^reportemaiz/$', views.reportemaizPage, name='reportemaizPage'),
    url(r'^reportecalificacionmaiz/$', views.reportecalificacionmaizPage, name='reportecalificacionmaizPage'),
    url(r'^escritura/$', views.escrituraPage, name='escrituraPage'),
    url(r'^api/escritura$', views.escritura, name='escritura'),
    url(r'^acciones/$', views.accionesPage, name='accionesPage'),
    url(r'^nuevo/$', views.enfermedadmaiz_view, name='enfermedadmaiz_crear'),
    url(r'^editar/(?P<id_enfermedadmaiz>\d+)/$', views.enfermedadmaiz_edit, name='enfermedadmaiz_editar'),
    url(r'^eliminar/(?P<id_enfermedadmaiz>\d+)/$', views.enfermedadmaiz_delete, name='enfermedadmaiz_eliminar'),
    #MAES
    url(r'^analisismaes/$', views.analisismaesPagina, name='analisismaesPagina'),
    url(r'^api/analisismaes$', views.agregarAnalisismaes, name='agregarAnalisismaes'),
    url(r'^api/reviewsmaes$', views.procesarCalificacionmaes, name='procesarCalificacionmaes'),
    url(r'^agregarmaes/$', views.nuevomaesEnfermedadPagina, name='nuevomaesEnfermedadPagina'),
    url(r'^api/enfermedadesmaes$', views.crearmaesEnfermedad, name='crearmaesEnfermedad'),
    url(r'^escrituramaes/$', views.escrituramaesPage, name='escrituramaesPage'),
    url(r'^api/escrituramaes$', views.escrituramaes, name='escrituramaes'),
    url(r'^reportemaesmaiz/$', views.reportemaesmaizPage, name='reportemaesmaizPage'),
    url(r'^reportecalificacionmaizmaes/$', views.reportecalificacionmaizmaesPage, name='reportecalificacionmaizmaesPage'),
    url(r'^accionesmaes/$', views.accionesmaesPage, name='accionesmaesPage'),
    url(r'^nuevomaes/$', views.enfermedadmaesmaiz_view, name='enfermedadmaesmaiz_crear'),
    url(r'^editarmaes/(?P<id_enfermedadmaesmaiz>\d+)/$', views.enfermedadmaesmaiz_edit, name='enfermedadmaesmaiz_editar'),
    url(r'^eliminarmaes/(?P<id_enfermedadmaesmaiz>\d+)/$', views.enfermedadmaesmaiz_delete, name='enfermedadmaesmaiz_eliminar'),
    #MARA
    url(r'^analisismara/$', views.analisismaraPagina, name='analisismaraPagina'),
    url(r'^api/analisismara$', views.agregarAnalisismara, name='agregarAnalisismara'),
    url(r'^api/reviewsmara$', views.procesarCalificacionmara, name='procesarCalificacionmara'),
    url(r'^agregarmara/$', views.nuevomaraEnfermedadPagina, name='nuevomaraEnfermedadPagina'),
    url(r'^api/enfermedadesmara$', views.crearmaraEnfermedad, name='crearmaraEnfermedad'),
    url(r'^escrituramara/$', views.escrituramaraPage, name='escrituramaraPage'),
    url(r'^api/escrituramara$', views.escrituramara, name='escrituramara'),
    url(r'^reportemaramaiz/$', views.reportemaramaizPage, name='reportemaramaizPage'),
    url(r'^reportecalificacionmaizmara/$', views.reportecalificacionmaizmaraPage, name='reportecalificacionmaizmaraPage'),
    url(r'^accionesmara/$', views.accionesmaraPage, name='accionesmaraPage'),
    url(r'^nuevomara/$', views.enfermedadmaramaiz_view, name='enfermedadmaramaiz_crear'),
    url(r'^editarmara/(?P<id_enfermedadmaramaiz>\d+)/$', views.enfermedadmaramaiz_edit, name='enfermedadmaramaiz_editar'),
    url(r'^eliminarmara/(?P<id_enfermedadmaramaiz>\d+)/$', views.enfermedadmaramaiz_delete, name='enfermedadmaramaiz_eliminar'),
    #SOHO
    url(r'^analisissoho/$', views.analisissohoPagina, name='analisissohoPagina'),
    url(r'^api/analisissoho$', views.agregarAnalisissoho, name='agregarAnalisissoho'),
    url(r'^api/reviewssoho$', views.procesarCalificacionsoho, name='procesarCalificacionsoho'),
    url(r'^agregarsoho/$', views.nuevosohoEnfermedadPagina, name='nuevosohoEnfermedadPagina'),
    url(r'^api/enfermedadessoho$', views.crearsohoEnfermedad, name='crearsohoEnfermedad'),
    url(r'^escriturasoho/$', views.escriturasohoPage, name='escriturasohoPage'),
    url(r'^api/escriturasoho$', views.escriturasoho, name='escriturasoho'),
    url(r'^reportesohomaiz/$', views.reportesohomaizPage, name='reportesohomaizPage'),
    url(r'^reportecalificacionmaizsoho/$', views.reportecalificacionmaizsohoPage, name='reportecalificacionmaizsohoPage'),
    url(r'^accionessoho/$', views.accionessohoPage, name='accionessohoPage'),
    url(r'^nuevosoho/$', views.enfermedadsohomaiz_view, name='enfermedadsohomaiz_crear'),
    url(r'^editarsoho/(?P<id_enfermedadsohomaiz>\d+)/$', views.enfermedadsohomaiz_edit, name='enfermedadsohomaiz_editar'),
    url(r'^eliminarsoho/(?P<id_enfermedadsohomaiz>\d+)/$', views.enfermedadsohomaiz_delete, name='enfermedadsohomaiz_eliminar'),
    #SOTA
    url(r'^analisissota/$', views.analisissotaPagina, name='analisissotaPagina'),
    url(r'^api/analisissota$', views.agregarAnalisissota, name='agregarAnalisissota'),
    url(r'^api/reviewssota$', views.procesarCalificacionsota, name='procesarCalificacionsota'),
    url(r'^agregarsota/$', views.nuevosotaEnfermedadPagina, name='nuevosotaEnfermedadPagina'),
    url(r'^api/enfermedadessota$', views.crearsotaEnfermedad, name='crearsotaEnfermedad'),
    url(r'^escriturasota/$', views.escriturasotaPage, name='escriturasotaPage'),
    url(r'^api/escriturasota$', views.escriturasota, name='escriturasota'),
    url(r'^reportesotamaiz/$', views.reportesotamaizPage, name='reportesotamaizPage'),
    url(r'^reportecalificacionmaizsota/$', views.reportecalificacionmaizsotaPage, name='reportecalificacionmaizsotaPage'),
    url(r'^accionessota/$', views.accionessotaPage, name='accionessotaPage'),
    url(r'^nuevosota/$', views.enfermedadsotamaiz_view, name='enfermedadsotamaiz_crear'),
    url(r'^editarsota/(?P<id_enfermedadsotamaiz>\d+)/$', views.enfermedadsotamaiz_edit, name='enfermedadsotamaiz_editar'),
    url(r'^eliminarsota/(?P<id_enfermedadsotamaiz>\d+)/$', views.enfermedadsotamaiz_delete, name='enfermedadsotamaiz_eliminar'),
    #SORA
    url(r'^analisissora/$', views.analisissoraPagina, name='analisissoraPagina'),
    url(r'^api/analisissora$', views.agregarAnalisissora, name='agregarAnalisissora'),
    url(r'^api/reviewssora$', views.procesarCalificacionsora, name='procesarCalificacionsora'),
    url(r'^agregarsora/$', views.nuevosoraEnfermedadPagina, name='nuevosoraEnfermedadPagina'),
    url(r'^api/enfermedadessora$', views.crearsoraEnfermedad, name='crearsoraEnfermedad'),
    url(r'^escriturasora/$', views.escriturasoraPage, name='escriturasoraPage'),
    url(r'^api/escriturasora$', views.escriturasora, name='escriturasora'),
    url(r'^reportesoramaiz/$', views.reportesoramaizPage, name='reportesoramaizPage'),
    url(r'^reportecalificacionmaizsora/$', views.reportecalificacionmaizsoraPage, name='reportecalificacionmaizsoraPage'),
    url(r'^accionessora/$', views.accionessoraPage, name='accionessoraPage'),
    url(r'^nuevosora/$', views.enfermedadsoramaiz_view, name='enfermedadsoramaiz_crear'),
    url(r'^editarsora/(?P<id_enfermedadsoramaiz>\d+)/$', views.enfermedadsoramaiz_edit, name='enfermedadsoramaiz_editar'),
    url(r'^eliminarsora/(?P<id_enfermedadsoramaiz>\d+)/$', views.enfermedadsoramaiz_delete, name='enfermedadsoramaiz_eliminar'),
    #TRIHO
    url(r'^analisistriho/$', views.analisistrihoPagina, name='analisistrihoPagina'),
    url(r'^api/analisistriho$', views.agregarAnalisistriho, name='agregarAnalisistriho'),
    url(r'^api/reviewstriho$', views.procesarCalificaciontriho, name='procesarCalificaciontriho'),
    url(r'^agregartriho/$', views.nuevotrihoEnfermedadPagina, name='nuevotrihoEnfermedadPagina'),
    url(r'^api/enfermedadestriho$', views.creartrihoEnfermedad, name='creartrihoEnfermedad'),
    url(r'^escrituratriho/$', views.escrituratrihoPage, name='escrituratrihoPage'),
    url(r'^api/escrituratriho$', views.escrituratriho, name='escrituratriho'),
    url(r'^reportetrihomaiz/$', views.reportetrihomaizPage, name='reportetrihomaizPage'),
    url(r'^reportecalificacionmaiztriho/$', views.reportecalificacionmaiztrihoPage, name='reportecalificacionmaiztrihoPage'),
    url(r'^accionestriho/$', views.accionestrihoPage, name='accionestrihoPage'),
    url(r'^nuevotriho/$', views.enfermedadtrihomaiz_view, name='enfermedadtrihomaiz_crear'),
    url(r'^editartriho/(?P<id_enfermedadtrihomaiz>\d+)/$', views.enfermedadtrihomaiz_edit, name='enfermedadtrihomaiz_editar'),
    url(r'^eliminartriho/(?P<id_enfermedadtrihomaiz>\d+)/$', views.enfermedadtrihomaiz_delete, name='enfermedadtrihomaiz_eliminar'),
    #TRIPLA
    url(r'^analisistripla/$', views.analisistriplaPagina, name='analisistriplaPagina'),
    url(r'^api/analisistripla$', views.agregarAnalisistripla, name='agregarAnalisistripla'),
    url(r'^api/reviewstripla$', views.procesarCalificaciontripla, name='procesarCalificaciontripla'),
    url(r'^agregartripla/$', views.nuevotriplaEnfermedadPagina, name='nuevotriplaEnfermedadPagina'),
    url(r'^api/enfermedadestripla$', views.creartriplaEnfermedad, name='creartriplaEnfermedad'),
    url(r'^escrituratripla/$', views.escrituratriplaPage, name='escrituratriplaPage'),
    url(r'^api/escrituratripla$', views.escrituratripla, name='escrituratripla'),
    url(r'^reportetriplamaiz/$', views.reportetriplamaizPage, name='reportetriplamaizPage'),
    url(r'^reportecalificacionmaiztripla/$', views.reportecalificacionmaiztriplaPage, name='reportecalificacionmaiztriplaPage'),
    url(r'^accionestripla/$', views.accionestriplaPage, name='accionestriplaPage'),
    url(r'^nuevotripla/$', views.enfermedadtriplamaiz_view, name='enfermedadtriplamaiz_crear'),
    url(r'^editartripla/(?P<id_enfermedadtriplamaiz>\d+)/$', views.enfermedadtriplamaiz_edit, name='enfermedadtriplamaiz_editar'),
    url(r'^eliminartripla/(?P<id_enfermedadtriplamaiz>\d+)/$', views.enfermedadtriplamaiz_delete, name='enfermedadtriplamaiz_eliminar'),
    #Varios
    url(r'^comentariouser/$', views.comentarioUser, name='comentarioUser'),
    url(r'^api/mireviews$', views.procesarMicalificacion, name='procesarMicalificacion'),
    url(r'^api/modifications$', views.modify, name='modify'),
    url(r'^reporte/$', views.reportePage, name='reportePage'),
    url(r'^reportedic/$', views.reportePagedic, name='reportePagedic'),
    url(r'^reportenov/$', views.reportePagenov, name='reportePagenov'),
    url(r'^reporteoct/$', views.reportePageoct, name='reportePageoct'),
    url(r'^reportesep/$', views.reportePagesep, name='reportePagesep'),
    url(r'^reporteago/$', views.reportePageago, name='reportePageago'),
]
