from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.http import HttpResponse
from miapp.models import Enfermedad, Review, Suggestion, Mireview, Enfermedadmaes, Enfermedadmara, Reviewmaes, Reviewmara, Enfermedadsoho, Reviewsoho, Enfermedadsota, Reviewsota, Enfermedadsora, Reviewsora, Enfermedadtriho, Reviewtriho, Enfermedadtripla, Reviewtripla
from PIL import Image, ImageOps
import datetime
import os.path
import clips
import ast
import time
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from miapp.forms import EnfermedadmaizForm, EnfermedadmaesmaizForm, EnfermedadmaramaizForm, EnfermedadsohomaizForm, EnfermedadsotamaizForm, EnfermedadsoramaizForm, EnfermedadtrihomaizForm, EnfermedadtriplamaizForm


def index(request):
    return render(request, 'index.html')


#inicio cf

def enfermedadmaiz_view(request):
    if request.method == 'POST':
        form = EnfermedadmaizForm(request.POST) 
        if form.is_valid():
            form.save()
        return redirect('enfermedadmaiz:index')
    else:
        form = EnfermedadmaizForm()
    return render(request, 'enfermedadmaiz_form.html', {'form':form})  


def enfermedadmaiz_edit(request,id_enfermedadmaiz):
    enfermedadmaiz = Enfermedad.objects.get(id=id_enfermedadmaiz)     
    if request.method == 'GET':
        form = EnfermedadmaizForm(instance=enfermedadmaiz)
    else:
        form = EnfermedadmaizForm(request.POST, instance=enfermedadmaiz)
        if form.is_valid():
            form.save()
        return redirect('accionesPage')
    return render(request, 'enfermedadmaiz_form.html', {'form':form}) 


def enfermedadmaiz_delete(request, id_enfermedadmaiz):
    enfermedadmaiz = Enfermedad.objects.get(id=id_enfermedadmaiz)
    if request.method == 'POST':
        enfermedadmaiz.delete()
        return redirect('accionesPage')
    return render(request,'enfermedadmaiz_delete.html', {'enfermedadmaiz':enfermedadmaiz}) 

#fin cf    


def analisisPagina(request):
    return render(request, 'analisis.html')


def analisismaesPagina(request):
    return render(request, 'analisismaes.html')  


def analisismaraPagina(request):
    return render(request, 'analisismara.html')


def analisissohoPagina(request):
    return render(request, 'analisissoho.html')          

@login_required
def nuevoEnfermedadPagina(request):
    return render(request, 'agregar.html')


def comentarioUser(request):
    return render(request, 'comentariouser.html')

@login_required
def reportePage(request):
    mireviews = Mireview.objects.order_by('-createdTime')
    return render(request, 'reporte.html', {'mireviews':mireviews})

@login_required
def reportePagedic(request):
    mireviews = Mireview.objects.filter(createdTime__contains='12').order_by('-createdTime')
    return render(request, 'reportedic.html', {'mireviews':mireviews})

@login_required
def reportePagenov(request):
    mireviews = Mireview.objects.filter(createdTime__contains='11').order_by('-createdTime')
    return render(request, 'reportenov.html', {'mireviews':mireviews})

@login_required
def reportePageoct(request):
    mireviews = Mireview.objects.filter(createdTime__contains='10').order_by('-createdTime')
    return render(request, 'reporteoct.html', {'mireviews':mireviews})


@login_required
def reportePagesep(request):
    mireviews = Mireview.objects.filter(createdTime__contains='09').order_by('-createdTime')
    return render(request, 'reportesep.html', {'mireviews':mireviews})   

@login_required
def reportePageago(request):
    mireviews = Mireview.objects.filter(createdTime__contains='08').order_by('-createdTime')
    return render(request, 'reporteago.html', {'mireviews':mireviews})  


@login_required
def reportemaizPage(request):
    enfermedadmaiz = Enfermedad.objects.all()
    return render(request, 'reportemaiz.html', {'enfermedadmaiz':enfermedadmaiz})


@login_required
def reportecalificacionmaizPage(request):
    reviewmaiz = Review.objects.order_by('-stars')
    return render(request, 'reportecalificacionmaiz.html', {'reviewmaiz':reviewmaiz})


@login_required
def accionesPage(request):
    enfermedadmaiz = Enfermedad.objects.all()
    return render(request, 'acciones.html', {'enfermedadmaiz':enfermedadmaiz})    


@csrf_exempt
def escrituraPage(request):
    enfermedadmaiz = Enfermedad.objects.latest('id')
    return render(request, 'escritura.html', {'enfermedadmaiz':enfermedadmaiz})       


@csrf_exempt
def escritura(request):
  
  if request.method == "POST":
    insertarCalificacionSE()
    return render(request, 'escritura.html')        



@csrf_exempt
def procesarCalificacion(request):
    if request.method == "POST":
        id = insertarCalificacionBD(request.POST)
        insertarCalificacionSE(request.POST, id)
        return HttpResponse('')
    else:
        response = []
        reviews = Review.objects.filter(enfermedadId=int(request.GET['enfermedadId'])).order_by("-id")
        for review in reviews:
            response.append({"id": review.id, "comment": review.comment, "reviewer": review.reviewer,
                    "createdTime": review.createdTime})
        return JsonResponse(response, safe=False)


@csrf_exempt
def procesarMicalificacion(request):
    if request.method == "POST":
        id = insertMireviewIntoDatabase(request.POST)
        return HttpResponse('')


@csrf_exempt
def crearEnfermedad(request):
    id = insertarNuevaEnfermedad(request.POST)
    insertIntoClips(id, request.POST)
    return HttpResponse('')



@csrf_exempt
def agregarAnalisis(request):
    result = seInferAnalisis(request.POST)
    print(result)
    response = []
    if result != None:
        for val in result.split('---'):
            if "," in val:
                val2 = val.split(',')
                enfermedad = Enfermedad.objects.get(id=int(val2[0]))
                response.append({"id": enfermedad.id, "name": enfermedad.name, "images": enfermedad.images, "description": enfermedad.description,
                    "planta": val2[1], "sintomaAAA": val2[2], "sintomaBB": val2[3], 
                    "sintomaCC": val2[4], "sintomaDD": val2[5], "sintomaEE": val2[6],
                    "stars": float(val2[7])})

    return JsonResponse(response, safe=False)



@csrf_exempt
def agregarAnalisismaes(request):
    result = seInferAnalisismaes(request.POST)
    print(result)
    response = []
    if result != None:
        for val in result.split('---'):
            if "," in val:
                val2 = val.split(',')
                enfermedadmaes = Enfermedadmaes.objects.get(id=int(val2[0]))
                response.append({"id": enfermedadmaes.id, "name": enfermedadmaes.name, "images": enfermedadmaes.images, "description": enfermedadmaes.description,
                    "planta": val2[1], "sintomaAAA": val2[2], "sintomaBB": val2[3], 
                    "sintomaCC": val2[4],
                    "stars": float(val2[5])})

    return JsonResponse(response, safe=False)


@csrf_exempt
def agregarAnalisismara(request):
    result = seInferAnalisismara(request.POST)
    print(result)
    response = []
    if result != None:
        for val in result.split('---'):
            if "," in val:
                val2 = val.split(',')
                enfermedadmara = Enfermedadmara.objects.get(id=int(val2[0]))
                response.append({"id": enfermedadmara.id, "name": enfermedadmara.name, "images": enfermedadmara.images, "description": enfermedadmara.description,
                    "planta": val2[1], "sintomaAAA": val2[2], "sintomaBB": val2[3], 
                    "sintomaCC": val2[4], "sintomaDD": val2[5], "sintomaEE": val2[6],
                    "stars": float(val2[7])})

    return JsonResponse(response, safe=False)



@csrf_exempt
def agregarAnalisissoho(request):
    result = seInferAnalisissoho(request.POST)
    print(result)
    response = []
    if result != None:
        for val in result.split('---'):
            if "," in val:
                val2 = val.split(',')
                enfermedadsoho = Enfermedadsoho.objects.get(id=int(val2[0]))
                response.append({"id": enfermedadsoho.id, "name": enfermedadsoho.name, "images": enfermedadsoho.images, "description": enfermedadsoho.description,
                    "planta": val2[1], "sintomaAAA": val2[2], "sintomaBB": val2[3], 
                    "sintomaCC": val2[4], "sintomaDD": val2[5], "sintomaEE": val2[6],
                    "stars": float(val2[7])})

    return JsonResponse(response, safe=False)    



@csrf_exempt
def modify(request):
    insertSuggestionIntoDatabase(request.POST)
    insertSuggestionsIntoClips()
    return HttpResponse('')



def insertarNuevaEnfermedad(data):
    images = ast.literal_eval(data['images'])
    imageNum = 0;
    for image in images:
        imageNum = imageNum + (image != 'null')

    enfermedad = Enfermedad(name=data['name'],
                description=data['description'],
                images=imageNum,
                planta=data['planta'],
                sintomaAA=data['sintomaAA'],
                sintomaBB=data['sintomaBB'],
                sintomaCC=data['sintomaCC'],
                sintomaEE=data['sintomaEE'],
                sintomaDD=data['sintomaDD'])
    enfermedad.save()

    index = 0
    for image in images:
        if image != 'null':
            index = index + 1
            createImage(enfermedad.id, index, image)

    return enfermedad.id


def createImage(id, index, image):
    imgCore = image.split(',')[1]
    imgFile = open(settings.ENFERMEDAD_IMAGEN_DIR + "/" + str(id) + "_" + str(index) + ".jpeg", "wb")
    imgFile.write(imgCore.decode('base64'))
    imgFile.close()

    
    img = Image.open(settings.ENFERMEDAD_IMAGEN_DIR + "/" + str(id) + "_" + str(index) + ".jpeg")
    longer_side = max(img.size)
    thumb = Image.new('RGBA', (longer_side, longer_side), (255, 255, 255, 0))
    thumb.paste(
        img, ((longer_side - img.size[0]) / 2, (longer_side - img.size[1]) / 2)
    )
    thumb.save(settings.ENFERMEDAD_IMAGEN_DIR + "/" + str(id) + "_" + str(index) + "_square.jpeg")


def insertIntoClips(id, data):
    
    FactsFile = settings.CLIPS_DIR + "/enfermedades.clp"
    if not os.path.isfile(FactsFile):
        file = open(FactsFile, 'w+')
        file.write("(deffacts enfermedades)\n")
        file.close()

   
    lines = open(FactsFile, 'r+').readlines()
    n = len(lines)
    lines[n - 1] = lines[n-1][:-2] + "\n"
    lines.append('  (enfermedad '
                '(ID '+str(id)+')'
                '(name "'+data['name']+'") '
                '(planta "'+data['planta']+'") '
                '(sintoma-aa "'+data['sintomaAA']+'") '
                '(sintoma-bb "'+data['sintomaBB']+'") '
                '(sintoma-cc "'+data['sintomaCC']+'") '
                '(sintoma-ee "'+data['sintomaEE']+'") '
                '(sintoma-dd "'+data['sintomaDD']+'") '
                '(stars -1)))\n')

    
    open(FactsFile, 'w').writelines(lines)


attributeMap = { 'sintomaAA': 'sintoma-aa',
        'sintomaBB': 'sintoma-bb',
        'sintomaCC': 'sintoma-cc',
        'sintomaDD': 'sintoma-dd',
        'sintomaEE': 'sintoma-ee'};
def insertSuggestionIntoDatabase(data):
    suggestion = Suggestion(
                enfermedadName=data['enfermedadName'],
                enfermedadId=int(data['enfermedadId']),
                attribute=attributeMap[data['key']],
                value=data['value'],
                quantity=0)

    suggestions = Suggestion.objects.filter(enfermedadId=int(data['enfermedadId']), attribute=attributeMap[data['key']], value=data['value'])
    if (len(suggestions) != 0):
        suggestion = suggestions[0]

    suggestion.quantity = suggestion.quantity + 1
    suggestion.save()
    print(suggestion)


def insertSuggestionsIntoClips():
    
    FactsFile = settings.CLIPS_DIR + "/suggestions.clp"
    if not os.path.isfile(FactsFile):
        file = open(FactsFile, 'w+')
        file.write("(deffacts suggestions)\n")
        file.close()

    
    suggestions = Suggestion.objects.all()
    lines = ['(deffacts suggestions\n']
    for suggestion in suggestions:
        lines.append('  (suggestion '
                     '(enfermedad-name "'+suggestion.enfermedadName+'")'
                     '(enfermedad-id '+str(suggestion.enfermedadId)+')'
                     '(attribute "'+suggestion.attribute+'")'
                     '(value "'+suggestion.value+'")'
                     '(quantity '+str(suggestion.quantity)+'))\n')

    lines.append(')\n')

    
    open(FactsFile, 'w').writelines(lines)


def insertarCalificacionBD(data):
    review = Review(reviewer=data['reviewer'],
                comment=data['comment'],
                stars=float(data['stars']),
                enfermedadName=data['enfermedadName'],
                enfermedadId=int(data['enfermedadId']),
                createdTime=datetime.datetime.now())
    print(review)
    review.save()
    return review.id


def insertarCalificacionSE(data, id):
    
    FactsFile = settings.XTRAS_DIR + "/calificaciones.clp"
    if not os.path.isfile(FactsFile):
        file = open(FactsFile, 'w+')
        file.write("(deffacts reviews)\n")
        file.close()

    
    lines = open(FactsFile, 'r+').readlines()
    n = len(lines)
    lines[n - 1] = lines[n-1][:-2] + "\n"
    lines.append('  (review '
                '(ID '+str(id)+')'
                '(enfermedad-name "'+data['enfermedadName']+'")'
                '(enfermedad-id '+data['enfermedadId']+')'
                '(reviewer "'+data['reviewer']+'")'
                '(comment "'+data['comment']+'")'
                '(stars '+data['stars']+')))\n')

    open(FactsFile, 'w').writelines(lines)


# INICIO NUEVO BONJOUR-----------------------------------------------------------------

def insertarCalificacionSE():
    FactsFile = settings.CLIPS_DIR + "/enfermedades.clp"
    if not os.path.isfile(FactsFile):
        file = open(FactsFile, 'w+')
        file.write("(deffacts enfermedades)\n")
        file.close()

    #nuevalinea
    suggestions = Enfermedad.objects.all()
    #finnuevalinea
    lines = ['(deffacts enfermedades\n']
    for suggestion in suggestions:
        lines.append('    (enfermedad '
                        '(ID '+str(suggestion.id)+')'
                        '(name "'+str(suggestion.name)+'") '
                        '(planta "'+str(suggestion.planta)+'") '
                        '(sintoma-aa "'+str(suggestion.sintomaAA)+'") '
                        '(sintoma-bb "'+str(suggestion.sintomaBB)+'") '
                        '(sintoma-cc "'+str(suggestion.sintomaCC)+'") '
                        '(sintoma-dd "'+str(suggestion.sintomaDD)+'") '
                        '(sintoma-ee "'+str(suggestion.sintomaEE)+'") '
                        '(stars -1))\n')

    lines.append(')\n')


#    open(FactsFile, 'w').writelines(lines)  
    open(FactsFile, 'w').writelines(lines)   

# FIN NUEVO BONJOUR--------------------------------------------------------------------


#MIO hahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahaha
def insertMireviewIntoDatabase(data):
    review = Mireview(reviewer=data['reviewer'],
                comment=data['comment'],
                createdTime=datetime.datetime.now())
    print(review)
    review.save()
    return review.id      


def seInferAnalisis(data):
    
    analisis = '(analisis ' +\
                 '(planta "'+data['planta']+'") ' +\
                 '(sintoma-aa "'+data['sintomaAA']+'") ' +\
                 '(sintoma-bb "'+data['sintomaBB']+'") ' +\
                 '(sintoma-cc "'+data['sintomaCC']+'") ' +\
                 '(sintoma-ee "'+data['sintomaEE']+'") ' +\
                 '(sintoma-dd "'+data['sintomaDD']+'"))'

    
    clips.Clear()
    clips.BatchStar(settings.CLIPS_DIR + "/templates.clp")
    if os.path.isfile(settings.CLIPS_DIR + "/enfermedades.clp"):
        clips.BatchStar(settings.CLIPS_DIR + "/enfermedades.clp")
    if os.path.isfile(settings.XTRAS_DIR + "/calificaciones.clp"):
        clips.BatchStar(settings.XTRAS_DIR + "/calificaciones.clp")
    clips.BatchStar(settings.CLIPS_DIR + "/reglas.clp")
    clips.Reset()
    clips.Assert(analisis)
    clips.Run()
    return clips.StdoutStream.Read()


def seInferAnalisismaes(data):
    
    analisis = '(analisis ' +\
                 '(planta "'+data['planta']+'") ' +\
                 '(sintoma-aa "'+data['sintomaAA']+'") ' +\
                 '(sintoma-bb "'+data['sintomaBB']+'") ' +\
                 '(sintoma-cc "'+data['sintomaCC']+'"))'                                  

    
    clips.Clear()
    clips.BatchStar(settings.CLIPS_DIR + "/templatesmaes.clp")
    if os.path.isfile(settings.CLIPS_DIR + "/enfermedadesmaes.clp"):
        clips.BatchStar(settings.CLIPS_DIR + "/enfermedadesmaes.clp")
    if os.path.isfile(settings.XTRAS_DIR + "/calificacionesmaes.clp"):
        clips.BatchStar(settings.XTRAS_DIR + "/calificacionesmaes.clp")
    clips.BatchStar(settings.CLIPS_DIR + "/reglasmaes.clp")
    clips.Reset()
    clips.Assert(analisis)
    clips.Run()
    return clips.StdoutStream.Read()


def seInferAnalisismara(data):
    
    analisis = '(analisis ' +\
                 '(planta "'+data['planta']+'") ' +\
                 '(sintoma-aa "'+data['sintomaAA']+'") ' +\
                 '(sintoma-bb "'+data['sintomaBB']+'") ' +\
                 '(sintoma-cc "'+data['sintomaCC']+'") ' +\
                 '(sintoma-ee "'+data['sintomaEE']+'") ' +\
                 '(sintoma-dd "'+data['sintomaDD']+'"))'

    
    clips.Clear()
    clips.BatchStar(settings.CLIPS_DIR + "/templatesmara.clp")
    if os.path.isfile(settings.CLIPS_DIR + "/enfermedadesmara.clp"):
        clips.BatchStar(settings.CLIPS_DIR + "/enfermedadesmara.clp")
    if os.path.isfile(settings.XTRAS_DIR + "/calificacionesmara.clp"):
        clips.BatchStar(settings.XTRAS_DIR + "/calificacionesmara.clp")
    clips.BatchStar(settings.CLIPS_DIR + "/reglasmara.clp")
    clips.Reset()
    clips.Assert(analisis)
    clips.Run()
    return clips.StdoutStream.Read()


def seInferAnalisissoho(data):
    
    analisis = '(analisis ' +\
                 '(planta "'+data['planta']+'") ' +\
                 '(sintoma-aa "'+data['sintomaAA']+'") ' +\
                 '(sintoma-bb "'+data['sintomaBB']+'") ' +\
                 '(sintoma-cc "'+data['sintomaCC']+'") ' +\
                 '(sintoma-ee "'+data['sintomaEE']+'") ' +\
                 '(sintoma-dd "'+data['sintomaDD']+'"))'

    
    clips.Clear()
    clips.BatchStar(settings.CLIPS_DIR + "/templatessoho.clp")
    if os.path.isfile(settings.CLIPS_DIR + "/enfermedadessoho.clp"):
        clips.BatchStar(settings.CLIPS_DIR + "/enfermedadessoho.clp")
    if os.path.isfile(settings.XTRAS_DIR + "/calificacionessoho.clp"):
        clips.BatchStar(settings.XTRAS_DIR + "/calificacionessoho.clp")
    clips.BatchStar(settings.CLIPS_DIR + "/reglassoho.clp")
    clips.Reset()
    clips.Assert(analisis)
    clips.Run()
    return clips.StdoutStream.Read()

#MAES--------------------------------------------------------------

@login_required
def nuevomaesEnfermedadPagina(request):
    return render(request, 'agregarmaes.html')



@csrf_exempt
def crearmaesEnfermedad(request):
    id = insertarmaesNuevaEnfermedad(request.POST)
#    insertIntoClips(id, request.POST)
    return HttpResponse('')



def insertarmaesNuevaEnfermedad(data):
    images = ast.literal_eval(data['images'])
    imageNum = 0;
    for image in images:
        imageNum = imageNum + (image != 'null')

    enfermedadmaes = Enfermedadmaes(name=data['name'],
                description=data['description'],
                images=imageNum,
                planta=data['planta'],
                sintomaAA=data['sintomaAA'],
                sintomaBB=data['sintomaBB'],
                sintomaCC=data['sintomaCC'])
    enfermedadmaes.save()

    index = 0
    for image in images:
        if image != 'null':
            index = index + 1
            createmaesImage(enfermedadmaes.id, index, image)

    return enfermedadmaes.id


def createmaesImage(id, index, image):
    imgCore = image.split(',')[1]
    imgFile = open(settings.ENFERMEDADMAES_IMAGEN_DIR + "/" + str(id) + "_" + str(index) + ".jpeg", "wb")
    imgFile.write(imgCore.decode('base64'))
    imgFile.close()

    # Create square image
    img = Image.open(settings.ENFERMEDADMAES_IMAGEN_DIR + "/" + str(id) + "_" + str(index) + ".jpeg")
    longer_side = max(img.size)
    thumb = Image.new('RGBA', (longer_side, longer_side), (255, 255, 255, 0))
    thumb.paste(
        img, ((longer_side - img.size[0]) / 2, (longer_side - img.size[1]) / 2)
    )
    thumb.save(settings.ENFERMEDADMAES_IMAGEN_DIR + "/" + str(id) + "_" + str(index) + "_square.jpeg")


@csrf_exempt
def escrituramaesPage(request):
    enfermedadmaesmaiz = Enfermedadmaes.objects.latest('id')
    return render(request, 'escrituramaes.html', {'enfermedadmaesmaiz':enfermedadmaesmaiz})       


@csrf_exempt
def escrituramaes(request):
  
  if request.method == "POST":
    insertarCalificacionmaesSE()
    return render(request, 'escrituramaes.html')


# INICIO NUEVO BONJOUR---------

def insertarCalificacionmaesSE():
    FactsFile = settings.CLIPS_DIR + "/enfermedadesmaes.clp"
    if not os.path.isfile(FactsFile):
        file = open(FactsFile, 'w+')
        file.write("(deffacts enfermedades)\n")
        file.close()

    #nuevalinea
    suggestions = Enfermedadmaes.objects.all()
    #finnuevalinea
    lines = ['(deffacts enfermedades\n']
    for suggestion in suggestions:
        lines.append('    (enfermedad '
                        '(ID '+str(suggestion.id)+')'
                        '(name "'+str(suggestion.name)+'") '
                        '(planta "'+str(suggestion.planta)+'") '
                        '(sintoma-aa "'+str(suggestion.sintomaAA)+'") '
                        '(sintoma-bb "'+str(suggestion.sintomaBB)+'") '
                        '(sintoma-cc "'+str(suggestion.sintomaCC)+'") '
                        '(stars -1))\n')

    lines.append(')\n')

    # new facts
#    open(FactsFile, 'w').writelines(lines)  
    open(FactsFile, 'w').writelines(lines)   

# FIN NUEVO BONJOUR----------

@login_required
def reportemaesmaizPage(request):
    enfermedadmaesmaiz = Enfermedadmaes.objects.all()
    return render(request, 'reportemaesmaiz.html', {'enfermedadmaesmaiz':enfermedadmaesmaiz})


#inicio cf

def enfermedadmaesmaiz_view(request):
    if request.method == 'POST':
        form = EnfermedadmaesmaizForm(request.POST) 
        if form.is_valid():
            form.save()
        return redirect('enfermedadmaesmaiz:index')
    else:
        form = EnfermedadmaesmaizForm()
    return render(request, 'enfermedadmaesmaiz_form.html', {'form':form})  


def enfermedadmaesmaiz_edit(request,id_enfermedadmaesmaiz):
    enfermedadmaesmaiz = Enfermedadmaes.objects.get(id=id_enfermedadmaesmaiz)     
    if request.method == 'GET':
        form = EnfermedadmaesmaizForm(instance=enfermedadmaesmaiz)
    else:
        form = EnfermedadmaesmaizForm(request.POST, instance=enfermedadmaesmaiz)
        if form.is_valid():
            form.save()
        return redirect('accionesmaesPage')
    return render(request, 'enfermedadmaesmaiz_form.html', {'form':form}) 


def enfermedadmaesmaiz_delete(request, id_enfermedadmaesmaiz):
    enfermedadmaesmaiz = Enfermedadmaes.objects.get(id=id_enfermedadmaesmaiz)
    if request.method == 'POST':
        enfermedadmaesmaiz.delete()
        return redirect('accionesmaesPage')
    return render(request,'enfermedadmaesmaiz_delete.html', {'enfermedadmaesmaiz':enfermedadmaesmaiz}) 

#fin cf


@csrf_exempt
def procesarCalificacionmaes(request):
    if request.method == "POST":
        id = insertarCalificacionmaesBD(request.POST)
        insertarCalificacionmaesSE(request.POST, id)
        return HttpResponse('')
    else:
        response = []
        reviews = Reviewmaes.objects.filter(enfermedadId=int(request.GET['enfermedadId'])).order_by("-id")
        for review in reviews:
            response.append({"id": review.id, "comment": review.comment, "reviewer": review.reviewer,
                    "createdTime": review.createdTime})
        return JsonResponse(response, safe=False)


def insertarCalificacionmaesBD(data):
    review = Reviewmaes(reviewer=data['reviewer'],
                comment=data['comment'],
                stars=float(data['stars']),
                enfermedadName=data['enfermedadName'],
                enfermedadId=int(data['enfermedadId']),
                createdTime=datetime.datetime.now())
    print(review)
    review.save()
    return review.id


def insertarCalificacionmaesSE(data, id):
    
    FactsFile = settings.XTRAS_DIR + "/calificacionesmaes.clp"
    if not os.path.isfile(FactsFile):
        file = open(FactsFile, 'w+')
        file.write("(deffacts reviews)\n")
        file.close()

    
    lines = open(FactsFile, 'r+').readlines()
    n = len(lines)
    lines[n - 1] = lines[n-1][:-2] + "\n"
    lines.append('  (review '
                '(ID '+str(id)+')'
                '(enfermedad-name "'+data['enfermedadName']+'")'
                '(enfermedad-id '+data['enfermedadId']+')'
                '(reviewer "'+data['reviewer']+'")'
                '(comment "'+data['comment']+'")'
                '(stars '+data['stars']+')))\n')

    
    open(FactsFile, 'w').writelines(lines)


@login_required
def reportecalificacionmaizmaesPage(request):
    reviewmaiz = Reviewmaes.objects.order_by('-stars')
    return render(request, 'reportecalificacionmaizmaes.html', {'reviewmaiz':reviewmaiz})

#MARA-----------------------------------------------------------------


@login_required
def nuevomaraEnfermedadPagina(request):
    return render(request, 'agregarmara.html')



@csrf_exempt
def crearmaraEnfermedad(request):
    id = insertarmaraNuevaEnfermedad(request.POST)

    return HttpResponse('')



def insertarmaraNuevaEnfermedad(data):
    images = ast.literal_eval(data['images'])
    imageNum = 0;
    for image in images:
        imageNum = imageNum + (image != 'null')

    enfermedadmara = Enfermedadmara(name=data['name'],
                description=data['description'],
                images=imageNum,
                planta=data['planta'],
                sintomaAA=data['sintomaAA'],
                sintomaBB=data['sintomaBB'],
                sintomaCC=data['sintomaCC'],
                sintomaEE=data['sintomaEE'],
                sintomaDD=data['sintomaDD'])
    enfermedadmara.save()

    index = 0
    for image in images:
        if image != 'null':
            index = index + 1
            createmaraImage(enfermedadmara.id, index, image)

    return enfermedadmara.id


def createmaraImage(id, index, image):
    imgCore = image.split(',')[1]
    imgFile = open(settings.ENFERMEDADMARA_IMAGEN_DIR + "/" + str(id) + "_" + str(index) + ".jpeg", "wb")
    imgFile.write(imgCore.decode('base64'))
    imgFile.close()

    # Create square image
    img = Image.open(settings.ENFERMEDADMARA_IMAGEN_DIR + "/" + str(id) + "_" + str(index) + ".jpeg")
    longer_side = max(img.size)
    thumb = Image.new('RGBA', (longer_side, longer_side), (255, 255, 255, 0))
    thumb.paste(
        img, ((longer_side - img.size[0]) / 2, (longer_side - img.size[1]) / 2)
    )
    thumb.save(settings.ENFERMEDADMARA_IMAGEN_DIR + "/" + str(id) + "_" + str(index) + "_square.jpeg")


@csrf_exempt
def escrituramaraPage(request):
    enfermedadmaramaiz = Enfermedadmara.objects.latest('id')
    return render(request, 'escrituramara.html', {'enfermedadmaramaiz':enfermedadmaramaiz})       


@csrf_exempt
def escrituramara(request):
  
  if request.method == "POST":
    insertarCalificacionmaraSE()
    return render(request, 'escrituramara.html')


# INICIO NUEVO BONJOUR---------

def insertarCalificacionmaraSE():
    FactsFile = settings.CLIPS_DIR + "/enfermedadesmara.clp"
    if not os.path.isfile(FactsFile):
        file = open(FactsFile, 'w+')
        file.write("(deffacts enfermedades)\n")
        file.close()

    
    #nuevalinea
    suggestions = Enfermedadmara.objects.all()
    #finnuevalinea
    lines = ['(deffacts enfermedades\n']
    for suggestion in suggestions:
        lines.append('    (enfermedad '
                        '(ID '+str(suggestion.id)+')'
                        '(name "'+str(suggestion.name)+'") '
                        '(planta "'+str(suggestion.planta)+'") '
                        '(sintoma-aa "'+str(suggestion.sintomaAA)+'") '
                        '(sintoma-bb "'+str(suggestion.sintomaBB)+'") '
                        '(sintoma-cc "'+str(suggestion.sintomaCC)+'") '
                        '(sintoma-dd "'+str(suggestion.sintomaDD)+'") '
                        '(sintoma-ee "'+str(suggestion.sintomaEE)+'") '
                        '(stars -1))\n')

    lines.append(')\n')

    # new facts
#    open(FactsFile, 'w').writelines(lines)  
    open(FactsFile, 'w').writelines(lines)   

# FIN NUEVO BONJOUR----------

@login_required
def reportemaramaizPage(request):
    enfermedadmaramaiz = Enfermedadmara.objects.all()
    return render(request, 'reportemaramaiz.html', {'enfermedadmaramaiz':enfermedadmaramaiz})


@login_required
def accionesmaesPage(request):
    enfermedadmaesmaiz = Enfermedadmaes.objects.all()
    return render(request, 'accionesmaes.html', {'enfermedadmaesmaiz':enfermedadmaesmaiz}) 


@login_required
def accionesmaraPage(request):
    enfermedadmaramaiz = Enfermedadmara.objects.all()
    return render(request, 'accionesmara.html', {'enfermedadmaramaiz':enfermedadmaramaiz}) 


#inicio cf

def enfermedadmaramaiz_view(request):
    if request.method == 'POST':
        form = EnfermedadmaramaizForm(request.POST) 
        if form.is_valid():
            form.save()
        return redirect('enfermedadmaramaiz:index')
    else:
        form = EnfermedadmaramaizForm()
    return render(request, 'enfermedadmaramaiz_form.html', {'form':form})  


def enfermedadmaramaiz_edit(request,id_enfermedadmaramaiz):
    enfermedadmaramaiz = Enfermedadmara.objects.get(id=id_enfermedadmaramaiz)     
    if request.method == 'GET':
        form = EnfermedadmaramaizForm(instance=enfermedadmaramaiz)
    else:
        form = EnfermedadmaramaizForm(request.POST, instance=enfermedadmaramaiz)
        if form.is_valid():
            form.save()
        return redirect('accionesmaraPage')
    return render(request, 'enfermedadmaramaiz_form.html', {'form':form}) 


def enfermedadmaramaiz_delete(request, id_enfermedadmaramaiz):
    enfermedadmaramaiz = Enfermedadmara.objects.get(id=id_enfermedadmaramaiz)
    if request.method == 'POST':
        enfermedadmaramaiz.delete()
        return redirect('accionesmaraPage')
    return render(request,'enfermedadmaramaiz_delete.html', {'enfermedadmaramaiz':enfermedadmaramaiz}) 

#fin cf



@csrf_exempt
def procesarCalificacionmara(request):
    if request.method == "POST":
        id = insertarCalificacionmaraBD(request.POST)
        insertarCalificacionmaraSE(request.POST, id)
        return HttpResponse('')
    else:
        response = []
        reviews = Reviewmara.objects.filter(enfermedadId=int(request.GET['enfermedadId'])).order_by("-id")
        for review in reviews:
            response.append({"id": review.id, "comment": review.comment, "reviewer": review.reviewer,
                    "createdTime": review.createdTime})
        return JsonResponse(response, safe=False)


def insertarCalificacionmaraBD(data):
    review = Reviewmara(reviewer=data['reviewer'],
                comment=data['comment'],
                stars=float(data['stars']),
                enfermedadName=data['enfermedadName'],
                enfermedadId=int(data['enfermedadId']),
                createdTime=datetime.datetime.now())
    print(review)
    review.save()
    return review.id


def insertarCalificacionmaraSE(data, id):
    
    FactsFile = settings.XTRAS_DIR + "/calificacionesmara.clp"
    if not os.path.isfile(FactsFile):
        file = open(FactsFile, 'w+')
        file.write("(deffacts reviews)\n")
        file.close()

    
    lines = open(FactsFile, 'r+').readlines()
    n = len(lines)
    lines[n - 1] = lines[n-1][:-2] + "\n"
    lines.append('  (review '
                '(ID '+str(id)+')'
                '(enfermedad-name "'+data['enfermedadName']+'")'
                '(enfermedad-id '+data['enfermedadId']+')'
                '(reviewer "'+data['reviewer']+'")'
                '(comment "'+data['comment']+'")'
                '(stars '+data['stars']+')))\n')

    
    open(FactsFile, 'w').writelines(lines)     


@login_required
def reportecalificacionmaizmaraPage(request):
    reviewmaiz = Reviewmara.objects.order_by('-stars')
    return render(request, 'reportecalificacionmaizmara.html', {'reviewmaiz':reviewmaiz})


#SOHO----------------------------------------------


@csrf_exempt
def procesarCalificacionsoho(request):
    if request.method == "POST":
        id = insertarCalificacionsohoBD(request.POST)
        insertarCalificacionsohoSE(request.POST, id)
        return HttpResponse('')
    else:
        response = []
        reviews = Reviewsoho.objects.filter(enfermedadId=int(request.GET['enfermedadId'])).order_by("-id")
        for review in reviews:
            response.append({"id": review.id, "comment": review.comment, "reviewer": review.reviewer,
                    "createdTime": review.createdTime})
        return JsonResponse(response, safe=False)


def insertarCalificacionsohoBD(data):
    review = Reviewsoho(reviewer=data['reviewer'],
                comment=data['comment'],
                stars=float(data['stars']),
                enfermedadName=data['enfermedadName'],
                enfermedadId=int(data['enfermedadId']),
                createdTime=datetime.datetime.now())
    print(review)
    review.save()
    return review.id


def insertarCalificacionsohoSE(data, id):
    
    FactsFile = settings.XTRAS_DIR + "/calificacionessoho.clp"
    if not os.path.isfile(FactsFile):
        file = open(FactsFile, 'w+')
        file.write("(deffacts reviews)\n")
        file.close()

    
    lines = open(FactsFile, 'r+').readlines()
    n = len(lines)
    lines[n - 1] = lines[n-1][:-2] + "\n"
    lines.append('  (review '
                '(ID '+str(id)+')'
                '(enfermedad-name "'+data['enfermedadName']+'")'
                '(enfermedad-id '+data['enfermedadId']+')'
                '(reviewer "'+data['reviewer']+'")'
                '(comment "'+data['comment']+'")'
                '(stars '+data['stars']+')))\n')

   
    open(FactsFile, 'w').writelines(lines)   


@login_required
def nuevosohoEnfermedadPagina(request):
    return render(request, 'agregarsoho.html')  



@csrf_exempt
def crearsohoEnfermedad(request):
    id = insertarsohoNuevaEnfermedad(request.POST)

    return HttpResponse('')



def insertarsohoNuevaEnfermedad(data):
    images = ast.literal_eval(data['images'])
    imageNum = 0;
    for image in images:
        imageNum = imageNum + (image != 'null')

    enfermedadsoho = Enfermedadsoho(name=data['name'],
                description=data['description'],
                images=imageNum,
                planta=data['planta'],
                sintomaAA=data['sintomaAA'],
                sintomaBB=data['sintomaBB'],
                sintomaCC=data['sintomaCC'],
                sintomaEE=data['sintomaEE'],
                sintomaDD=data['sintomaDD'])
    enfermedadsoho.save()

    index = 0
    for image in images:
        if image != 'null':
            index = index + 1
            createsohoImage(enfermedadsoho.id, index, image)

    return enfermedadsoho.id


def createsohoImage(id, index, image):
    imgCore = image.split(',')[1]
    imgFile = open(settings.ENFERMEDADSOHO_IMAGEN_DIR + "/" + str(id) + "_" + str(index) + ".jpeg", "wb")
    imgFile.write(imgCore.decode('base64'))
    imgFile.close()

    
    img = Image.open(settings.ENFERMEDADSOHO_IMAGEN_DIR + "/" + str(id) + "_" + str(index) + ".jpeg")
    longer_side = max(img.size)
    thumb = Image.new('RGBA', (longer_side, longer_side), (255, 255, 255, 0))
    thumb.paste(
        img, ((longer_side - img.size[0]) / 2, (longer_side - img.size[1]) / 2)
    )
    thumb.save(settings.ENFERMEDADSOHO_IMAGEN_DIR + "/" + str(id) + "_" + str(index) + "_square.jpeg")


@csrf_exempt
def escriturasohoPage(request):
    enfermedadsohomaiz = Enfermedadsoho.objects.latest('id')
    return render(request, 'escriturasoho.html', {'enfermedadsohomaiz':enfermedadsohomaiz})  


@csrf_exempt
def escriturasoho(request):
  
  if request.method == "POST":
    insertarCalificacionsohoSE()
    return render(request, 'escriturasoho.html')


# INICIO NUEVO BONJOUR---------

def insertarCalificacionsohoSE():
    FactsFile = settings.CLIPS_DIR + "/enfermedadessoho.clp"
    if not os.path.isfile(FactsFile):
        file = open(FactsFile, 'w+')
        file.write("(deffacts enfermedades)\n")
        file.close()

    
    #nuevalinea
    suggestions = Enfermedadsoho.objects.all()
    #finnuevalinea
    lines = ['(deffacts enfermedades\n']
    for suggestion in suggestions:
        lines.append('    (enfermedad '
                        '(ID '+str(suggestion.id)+')'
                        '(name "'+str(suggestion.name)+'") '
                        '(planta "'+str(suggestion.planta)+'") '
                        '(sintoma-aa "'+str(suggestion.sintomaAA)+'") '
                        '(sintoma-bb "'+str(suggestion.sintomaBB)+'") '
                        '(sintoma-cc "'+str(suggestion.sintomaCC)+'") '
                        '(sintoma-dd "'+str(suggestion.sintomaDD)+'") '
                        '(sintoma-ee "'+str(suggestion.sintomaEE)+'") '
                        '(stars -1))\n')

    lines.append(')\n')

    
#    open(FactsFile, 'w').writelines(lines)  
    open(FactsFile, 'w').writelines(lines)   

# FIN NUEVO BONJOUR----------


@login_required
def reportesohomaizPage(request):
    enfermedadsohomaiz = Enfermedadsoho.objects.all()
    return render(request, 'reportesohomaiz.html', {'enfermedadsohomaiz':enfermedadsohomaiz})


@login_required
def reportecalificacionmaizsohoPage(request):
    reviewmaiz = Reviewsoho.objects.order_by('-stars')
    return render(request, 'reportecalificacionmaizsoho.html', {'reviewmaiz':reviewmaiz})


@login_required
def accionessohoPage(request):
    enfermedadsohomaiz = Enfermedadsoho.objects.all()
    return render(request, 'accionessoho.html', {'enfermedadsohomaiz':enfermedadsohomaiz})


#inicio cf

def enfermedadsohomaiz_view(request):
    if request.method == 'POST':
        form = EnfermedadsohomaizForm(request.POST) 
        if form.is_valid():
            form.save()
        return redirect('enfermedadsohomaiz:index')
    else:
        form = EnfermedadsohomaizForm()
    return render(request, 'enfermedadsohomaiz_form.html', {'form':form})  


def enfermedadsohomaiz_edit(request,id_enfermedadsohomaiz):
    enfermedadsohomaiz = Enfermedadsoho.objects.get(id=id_enfermedadsohomaiz)     
    if request.method == 'GET':
        form = EnfermedadsohomaizForm(instance=enfermedadsohomaiz)
    else:
        form = EnfermedadsohomaizForm(request.POST, instance=enfermedadsohomaiz)
        if form.is_valid():
            form.save()
        return redirect('accionessohoPage')
    return render(request, 'enfermedadsohomaiz_form.html', {'form':form}) 


def enfermedadsohomaiz_delete(request, id_enfermedadsohomaiz):
    enfermedadsohomaiz = Enfermedadsoho.objects.get(id=id_enfermedadsohomaiz)
    if request.method == 'POST':
        enfermedadsohomaiz.delete()
        return redirect('accionessohoPage')
    return render(request,'enfermedadsohomaiz_delete.html', {'enfermedadsohomaiz':enfermedadsohomaiz}) 

#fin cf


#SOTA---------------------------------------

def analisissotaPagina(request):
    return render(request, 'analisissota.html')


@csrf_exempt
def agregarAnalisissota(request):
    result = seInferAnalisissota(request.POST)
    print(result)
    response = []
    if result != None:
        for val in result.split('---'):
            if "," in val:
                val2 = val.split(',')
                enfermedadsota = Enfermedadsota.objects.get(id=int(val2[0]))
                response.append({"id": enfermedadsota.id, "name": enfermedadsota.name, "images": enfermedadsota.images, "description": enfermedadsota.description,
                    "planta": val2[1], "sintomaAAA": val2[2], "sintomaBB": val2[3], 
                    "sintomaCC": val2[4], "sintomaDD": val2[5], 
                    "stars": float(val2[6])})

    return JsonResponse(response, safe=False)


def seInferAnalisissota(data):
    
    analisis = '(analisis ' +\
                 '(planta "'+data['planta']+'") ' +\
                 '(sintoma-aa "'+data['sintomaAA']+'") ' +\
                 '(sintoma-bb "'+data['sintomaBB']+'") ' +\
                 '(sintoma-cc "'+data['sintomaCC']+'") ' +\
                 '(sintoma-dd "'+data['sintomaDD']+'"))'

    
    clips.Clear()
    clips.BatchStar(settings.CLIPS_DIR + "/templatessota.clp")
    if os.path.isfile(settings.CLIPS_DIR + "/enfermedadessota.clp"):
        clips.BatchStar(settings.CLIPS_DIR + "/enfermedadessota.clp")
    if os.path.isfile(settings.XTRAS_DIR + "/calificacionessota.clp"):
        clips.BatchStar(settings.XTRAS_DIR + "/calificacionessota.clp")
    clips.BatchStar(settings.CLIPS_DIR + "/reglassota.clp")
    clips.Reset()
    clips.Assert(analisis)
    clips.Run()
    return clips.StdoutStream.Read()



@csrf_exempt
def procesarCalificacionsota(request):
    if request.method == "POST":
        id = insertarCalificacionsotaBD(request.POST)
        insertarCalificacionsotaSE(request.POST, id)
        return HttpResponse('')
    else:
        response = []
        reviews = Reviewsota.objects.filter(enfermedadId=int(request.GET['enfermedadId'])).order_by("-id")
        for review in reviews:
            response.append({"id": review.id, "comment": review.comment, "reviewer": review.reviewer,
                    "createdTime": review.createdTime})
        return JsonResponse(response, safe=False)


def insertarCalificacionsotaBD(data):
    review = Reviewsota(reviewer=data['reviewer'],
                comment=data['comment'],
                stars=float(data['stars']),
                enfermedadName=data['enfermedadName'],
                enfermedadId=int(data['enfermedadId']),
                createdTime=datetime.datetime.now())
    print(review)
    review.save()
    return review.id


def insertarCalificacionsotaSE(data, id):
    
    FactsFile = settings.XTRAS_DIR + "/calificacionessota.clp"
    if not os.path.isfile(FactsFile):
        file = open(FactsFile, 'w+')
        file.write("(deffacts reviews)\n")
        file.close()

    
    lines = open(FactsFile, 'r+').readlines()
    n = len(lines)
    lines[n - 1] = lines[n-1][:-2] + "\n"
    lines.append('  (review '
                '(ID '+str(id)+')'
                '(enfermedad-name "'+data['enfermedadName']+'")'
                '(enfermedad-id '+data['enfermedadId']+')'
                '(reviewer "'+data['reviewer']+'")'
                '(comment "'+data['comment']+'")'
                '(stars '+data['stars']+')))\n')

    
    open(FactsFile, 'w').writelines(lines)


@login_required
def nuevosotaEnfermedadPagina(request):
    return render(request, 'agregarsota.html')  



@csrf_exempt
def crearsotaEnfermedad(request):
    id = insertarsotaNuevaEnfermedad(request.POST)

    return HttpResponse('')



def insertarsotaNuevaEnfermedad(data):
    images = ast.literal_eval(data['images'])
    imageNum = 0;
    for image in images:
        imageNum = imageNum + (image != 'null')

    enfermedadsota = Enfermedadsota(name=data['name'],
                description=data['description'],
                images=imageNum,
                planta=data['planta'],
                sintomaAA=data['sintomaAA'],
                sintomaBB=data['sintomaBB'],
                sintomaCC=data['sintomaCC'],
                sintomaDD=data['sintomaDD'])
    enfermedadsota.save()

    index = 0
    for image in images:
        if image != 'null':
            index = index + 1
            createsotaImage(enfermedadsota.id, index, image)

    return enfermedadsota.id  


def createsotaImage(id, index, image):
    imgCore = image.split(',')[1]
    imgFile = open(settings.ENFERMEDADSOTA_IMAGEN_DIR + "/" + str(id) + "_" + str(index) + ".jpeg", "wb")
    imgFile.write(imgCore.decode('base64'))
    imgFile.close()

    
    img = Image.open(settings.ENFERMEDADSOTA_IMAGEN_DIR + "/" + str(id) + "_" + str(index) + ".jpeg")
    longer_side = max(img.size)
    thumb = Image.new('RGBA', (longer_side, longer_side), (255, 255, 255, 0))
    thumb.paste(
        img, ((longer_side - img.size[0]) / 2, (longer_side - img.size[1]) / 2)
    )
    thumb.save(settings.ENFERMEDADSOTA_IMAGEN_DIR + "/" + str(id) + "_" + str(index) + "_square.jpeg")   


@csrf_exempt
def escriturasotaPage(request):
    enfermedadsotamaiz = Enfermedadsota.objects.latest('id')
    return render(request, 'escriturasota.html', {'enfermedadsotamaiz':enfermedadsotamaiz})  


@csrf_exempt
def escriturasota(request):
  
  if request.method == "POST":
    insertarCalificacionsotaSE()
    return render(request, 'escriturasota.html')


# INICIO NUEVO BONJOUR---------

def insertarCalificacionsotaSE():
    FactsFile = settings.CLIPS_DIR + "/enfermedadessota.clp"
    if not os.path.isfile(FactsFile):
        file = open(FactsFile, 'w+')
        file.write("(deffacts enfermedades)\n")
        file.close()

    
    #nuevalinea
    suggestions = Enfermedadsota.objects.all()
    #finnuevalinea
    lines = ['(deffacts enfermedades\n']
    for suggestion in suggestions:
        lines.append('    (enfermedad '
                        '(ID '+str(suggestion.id)+')'
                        '(name "'+str(suggestion.name)+'") '
                        '(planta "'+str(suggestion.planta)+'") '
                        '(sintoma-aa "'+str(suggestion.sintomaAA)+'") '
                        '(sintoma-bb "'+str(suggestion.sintomaBB)+'") '
                        '(sintoma-cc "'+str(suggestion.sintomaCC)+'") '
                        '(sintoma-dd "'+str(suggestion.sintomaDD)+'") '
                        '(stars -1))\n')

    lines.append(')\n')

    # new facts
#    open(FactsFile, 'w').writelines(lines)  
    open(FactsFile, 'w').writelines(lines)   

# FIN NUEVO BONJOUR----------   


@login_required
def reportesotamaizPage(request):
    enfermedadsotamaiz = Enfermedadsota.objects.all()
    return render(request, 'reportesotamaiz.html', {'enfermedadsotamaiz':enfermedadsotamaiz})


@login_required
def reportecalificacionmaizsotaPage(request):
    reviewmaiz = Reviewsota.objects.order_by('-stars')
    return render(request, 'reportecalificacionmaizsota.html', {'reviewmaiz':reviewmaiz})  


@login_required
def accionessotaPage(request):
    enfermedadsotamaiz = Enfermedadsota.objects.all()
    return render(request, 'accionessota.html', {'enfermedadsotamaiz':enfermedadsotamaiz})


#inicio cf

def enfermedadsotamaiz_view(request):
    if request.method == 'POST':
        form = EnfermedadsotamaizForm(request.POST) 
        if form.is_valid():
            form.save()
        return redirect('enfermedadsotamaiz:index')
    else:
        form = EnfermedadsotamaizForm()
    return render(request, 'enfermedadsotamaiz_form.html', {'form':form})  


def enfermedadsotamaiz_edit(request,id_enfermedadsotamaiz):
    enfermedadsotamaiz = Enfermedadsota.objects.get(id=id_enfermedadsotamaiz)     
    if request.method == 'GET':
        form = EnfermedadsotamaizForm(instance=enfermedadsotamaiz)
    else:
        form = EnfermedadsotamaizForm(request.POST, instance=enfermedadsotamaiz)
        if form.is_valid():
            form.save()
        return redirect('accionessotaPage')
    return render(request, 'enfermedadsotamaiz_form.html', {'form':form}) 


def enfermedadsotamaiz_delete(request, id_enfermedadsotamaiz):
    enfermedadsotamaiz = Enfermedadsota.objects.get(id=id_enfermedadsotamaiz)
    if request.method == 'POST':
        enfermedadsotamaiz.delete()
        return redirect('accionessotaPage')
    return render(request,'enfermedadsotamaiz_delete.html', {'enfermedadsotamaiz':enfermedadsotamaiz}) 

#fin cf

#SORA---------------------------------------------------------------------------

def analisissoraPagina(request):
    return render(request, 'analisissora.html')

@csrf_exempt
def agregarAnalisissora(request):
    result = seInferAnalisissora(request.POST)
    print(result)
    response = []
    if result != None:
        for val in result.split('---'):
            if "," in val:
                val2 = val.split(',')
                enfermedadsora = Enfermedadsora.objects.get(id=int(val2[0]))
                response.append({"id": enfermedadsora.id, "name": enfermedadsora.name, "images": enfermedadsora.images, "description": enfermedadsora.description,
                    "planta": val2[1], "sintomaAAA": val2[2], "sintomaBB": val2[3], 
                    "sintomaCC": val2[4], "sintomaDD": val2[5], 
                    "stars": float(val2[6])})

    return JsonResponse(response, safe=False)


def seInferAnalisissora(data):
    
    analisis = '(analisis ' +\
                 '(planta "'+data['planta']+'") ' +\
                 '(sintoma-aa "'+data['sintomaAA']+'") ' +\
                 '(sintoma-bb "'+data['sintomaBB']+'") ' +\
                 '(sintoma-cc "'+data['sintomaCC']+'") ' +\
                 '(sintoma-dd "'+data['sintomaDD']+'"))'

    
    clips.Clear()
    clips.BatchStar(settings.CLIPS_DIR + "/templatessora.clp")
    if os.path.isfile(settings.CLIPS_DIR + "/enfermedadessora.clp"):
        clips.BatchStar(settings.CLIPS_DIR + "/enfermedadessora.clp")
    if os.path.isfile(settings.XTRAS_DIR + "/calificacionessora.clp"):
        clips.BatchStar(settings.XTRAS_DIR + "/calificacionessora.clp")
    clips.BatchStar(settings.CLIPS_DIR + "/reglassora.clp")
    clips.Reset()
    clips.Assert(analisis)
    clips.Run()
    return clips.StdoutStream.Read()



@csrf_exempt
def procesarCalificacionsora(request):
    if request.method == "POST":
        id = insertarCalificacionsoraBD(request.POST)
        insertarCalificacionsoraSE(request.POST, id)
        return HttpResponse('')
    else:
        response = []
        reviews = Reviewsora.objects.filter(enfermedadId=int(request.GET['enfermedadId'])).order_by("-id")
        for review in reviews:
            response.append({"id": review.id, "comment": review.comment, "reviewer": review.reviewer,
                    "createdTime": review.createdTime})
        return JsonResponse(response, safe=False)


def insertarCalificacionsoraBD(data):
    review = Reviewsora(reviewer=data['reviewer'],
                comment=data['comment'],
                stars=float(data['stars']),
                enfermedadName=data['enfermedadName'],
                enfermedadId=int(data['enfermedadId']),
                createdTime=datetime.datetime.now())
    print(review)
    review.save()
    return review.id


def insertarCalificacionsoraSE(data, id):
    # check if a fact-file exists
    FactsFile = settings.XTRAS_DIR + "/calificacionessora.clp"
    if not os.path.isfile(FactsFile):
        file = open(FactsFile, 'w+')
        file.write("(deffacts reviews)\n")
        file.close()

    # modify facts
    lines = open(FactsFile, 'r+').readlines()
    n = len(lines)
    lines[n - 1] = lines[n-1][:-2] + "\n"
    lines.append('  (review '
                '(ID '+str(id)+')'
                '(enfermedad-name "'+data['enfermedadName']+'")'
                '(enfermedad-id '+data['enfermedadId']+')'
                '(reviewer "'+data['reviewer']+'")'
                '(comment "'+data['comment']+'")'
                '(stars '+data['stars']+')))\n')

    # new facts
    open(FactsFile, 'w').writelines(lines)


@login_required
def nuevosoraEnfermedadPagina(request):
    return render(request, 'agregarsora.html')  



@csrf_exempt
def crearsoraEnfermedad(request):
    id = insertarsoraNuevaEnfermedad(request.POST)
    return HttpResponse('')


def insertarsoraNuevaEnfermedad(data):
    images = ast.literal_eval(data['images'])
    imageNum = 0;
    for image in images:
        imageNum = imageNum + (image != 'null')

    enfermedadsora = Enfermedadsora(name=data['name'],
                description=data['description'],
                images=imageNum,
                planta=data['planta'],
                sintomaAA=data['sintomaAA'],
                sintomaBB=data['sintomaBB'],
                sintomaCC=data['sintomaCC'],
                sintomaDD=data['sintomaDD'])
    enfermedadsora.save()

    index = 0
    for image in images:
        if image != 'null':
            index = index + 1
            createsoraImage(enfermedadsora.id, index, image)

    return enfermedadsora.id  


def createsoraImage(id, index, image):
    imgCore = image.split(',')[1]
    imgFile = open(settings.ENFERMEDADSORA_IMAGEN_DIR + "/" + str(id) + "_" + str(index) + ".jpeg", "wb")
    imgFile.write(imgCore.decode('base64'))
    imgFile.close()

    # Create square image
    img = Image.open(settings.ENFERMEDADSORA_IMAGEN_DIR + "/" + str(id) + "_" + str(index) + ".jpeg")
    longer_side = max(img.size)
    thumb = Image.new('RGBA', (longer_side, longer_side), (255, 255, 255, 0))
    thumb.paste(
        img, ((longer_side - img.size[0]) / 2, (longer_side - img.size[1]) / 2)
    )
    thumb.save(settings.ENFERMEDADSORA_IMAGEN_DIR + "/" + str(id) + "_" + str(index) + "_square.jpeg")


@csrf_exempt
def escriturasoraPage(request):
    enfermedadsoramaiz = Enfermedadsora.objects.latest('id')
    return render(request, 'escriturasora.html', {'enfermedadsoramaiz':enfermedadsoramaiz})  


@csrf_exempt
def escriturasora(request):
  
  if request.method == "POST":
    insertarCalificacionsoraSE()
    return render(request, 'escriturasora.html')



def insertarCalificacionsoraSE():
    FactsFile = settings.CLIPS_DIR + "/enfermedadessora.clp"
    if not os.path.isfile(FactsFile):
        file = open(FactsFile, 'w+')
        file.write("(deffacts enfermedades)\n")
        file.close()

        
    #nuevalinea
    suggestions = Enfermedadsora.objects.all()
    #finnuevalinea
    lines = ['(deffacts enfermedades\n']
    for suggestion in suggestions:
        lines.append('    (enfermedad '
                        '(ID '+str(suggestion.id)+')'
                        '(name "'+str(suggestion.name)+'") '
                        '(planta "'+str(suggestion.planta)+'") '
                        '(sintoma-aa "'+str(suggestion.sintomaAA)+'") '
                        '(sintoma-bb "'+str(suggestion.sintomaBB)+'") '
                        '(sintoma-cc "'+str(suggestion.sintomaCC)+'") '
                        '(sintoma-dd "'+str(suggestion.sintomaDD)+'") '
                        '(stars -1))\n')

    lines.append(')\n')

    # new facts
#    open(FactsFile, 'w').writelines(lines)  
    open(FactsFile, 'w').writelines(lines)   

# FIN NUEVO BONJOUR----------   


@login_required
def reportesoramaizPage(request):
    enfermedadsoramaiz = Enfermedadsora.objects.all()
    return render(request, 'reportesoramaiz.html', {'enfermedadsoramaiz':enfermedadsoramaiz})


@login_required
def reportecalificacionmaizsoraPage(request):
    reviewmaiz = Reviewsora.objects.order_by('-stars')
    return render(request, 'reportecalificacionmaizsora.html', {'reviewmaiz':reviewmaiz})


@login_required
def accionessoraPage(request):
    enfermedadsoramaiz = Enfermedadsora.objects.all()
    return render(request, 'accionessora.html', {'enfermedadsoramaiz':enfermedadsoramaiz}) 


#inicio cf

def enfermedadsoramaiz_view(request):
    if request.method == 'POST':
        form = EnfermedadsoramaizForm(request.POST) 
        if form.is_valid():
            form.save()
        return redirect('enfermedadsoramaiz:index')
    else:
        form = EnfermedadsoramaizForm()
    return render(request, 'enfermedadsoramaiz_form.html', {'form':form})  


def enfermedadsoramaiz_edit(request,id_enfermedadsoramaiz):
    enfermedadsoramaiz = Enfermedadsora.objects.get(id=id_enfermedadsoramaiz)     
    if request.method == 'GET':
        form = EnfermedadsoramaizForm(instance=enfermedadsoramaiz)
    else:
        form = EnfermedadsoramaizForm(request.POST, instance=enfermedadsoramaiz)
        if form.is_valid():
            form.save()
        return redirect('accionessoraPage')
    return render(request, 'enfermedadsoramaiz_form.html', {'form':form}) 


def enfermedadsoramaiz_delete(request, id_enfermedadsoramaiz):
    enfermedadsoramaiz = Enfermedadsora.objects.get(id=id_enfermedadsoramaiz)
    if request.method == 'POST':
        enfermedadsoramaiz.delete()
        return redirect('accionessoraPage')
    return render(request,'enfermedadsoramaiz_delete.html', {'enfermedadsoramaiz':enfermedadsoramaiz}) 

#fin cf


#TRIHO--------------------------------------------------------------------------

def analisistrihoPagina(request):
    return render(request, 'analisistriho.html')


@csrf_exempt
def agregarAnalisistriho(request):
    result = seInferAnalisistriho(request.POST)
    print(result)
    response = []
    if result != None:
        for val in result.split('---'):
            if "," in val:
                val2 = val.split(',')
                enfermedadtriho = Enfermedadtriho.objects.get(id=int(val2[0]))
                response.append({"id": enfermedadtriho.id, "name": enfermedadtriho.name, "images": enfermedadtriho.images, "description": enfermedadtriho.description,
                    "planta": val2[1], "sintomaAAA": val2[2], "sintomaBB": val2[3], 
                    "sintomaCC": val2[4],  
                    "stars": float(val2[5])})

    return JsonResponse(response, safe=False)


def seInferAnalisistriho(data):
    
    analisis = '(analisis ' +\
                 '(planta "'+data['planta']+'") ' +\
                 '(sintoma-aa "'+data['sintomaAA']+'") ' +\
                 '(sintoma-bb "'+data['sintomaBB']+'") ' +\
                 '(sintoma-cc "'+data['sintomaCC']+'"))' 

    
    clips.Clear()
    clips.BatchStar(settings.CLIPS_DIR + "/templatestriho.clp")
    if os.path.isfile(settings.CLIPS_DIR + "/enfermedadestriho.clp"):
        clips.BatchStar(settings.CLIPS_DIR + "/enfermedadestriho.clp")
    if os.path.isfile(settings.XTRAS_DIR + "/calificacionestriho.clp"):
        clips.BatchStar(settings.XTRAS_DIR + "/calificacionestriho.clp")
    clips.BatchStar(settings.CLIPS_DIR + "/reglastriho.clp")
    clips.Reset()
    clips.Assert(analisis)
    clips.Run()
    return clips.StdoutStream.Read()



@csrf_exempt
def procesarCalificaciontriho(request):
    if request.method == "POST":
        id = insertarCalificaciontrihoBD(request.POST)
        insertarCalificaciontrihoSE(request.POST, id)
        return HttpResponse('')
    else:
        response = []
        reviews = Reviewtriho.objects.filter(enfermedadId=int(request.GET['enfermedadId'])).order_by("-id")
        for review in reviews:
            response.append({"id": review.id, "comment": review.comment, "reviewer": review.reviewer,
                    "createdTime": review.createdTime})
        return JsonResponse(response, safe=False)


def insertarCalificaciontrihoBD(data):
    review = Reviewtriho(reviewer=data['reviewer'],
                comment=data['comment'],
                stars=float(data['stars']),
                enfermedadName=data['enfermedadName'],
                enfermedadId=int(data['enfermedadId']),
                createdTime=datetime.datetime.now())
    print(review)
    review.save()
    return review.id


def insertarCalificaciontrihoSE(data, id):
    
    FactsFile = settings.XTRAS_DIR + "/calificacionestriho.clp"
    if not os.path.isfile(FactsFile):
        file = open(FactsFile, 'w+')
        file.write("(deffacts reviews)\n")
        file.close()

    # modify facts
    lines = open(FactsFile, 'r+').readlines()
    n = len(lines)
    lines[n - 1] = lines[n-1][:-2] + "\n"
    lines.append('  (review '
                '(ID '+str(id)+')'
                '(enfermedad-name "'+data['enfermedadName']+'")'
                '(enfermedad-id '+data['enfermedadId']+')'
                '(reviewer "'+data['reviewer']+'")'
                '(comment "'+data['comment']+'")'
                '(stars '+data['stars']+')))\n')

    
    open(FactsFile, 'w').writelines(lines)


@login_required
def nuevotrihoEnfermedadPagina(request):
    return render(request, 'agregartriho.html')



@csrf_exempt
def creartrihoEnfermedad(request):
    id = insertartrihoNuevaEnfermedad(request.POST)

    return HttpResponse('')



def insertartrihoNuevaEnfermedad(data):
    images = ast.literal_eval(data['images'])
    imageNum = 0;
    for image in images:
        imageNum = imageNum + (image != 'null')

    enfermedadtriho = Enfermedadtriho(name=data['name'],
                description=data['description'],
                images=imageNum,
                planta=data['planta'],
                sintomaAA=data['sintomaAA'],
                sintomaBB=data['sintomaBB'],
                sintomaCC=data['sintomaCC'])
    enfermedadtriho.save()

    index = 0
    for image in images:
        if image != 'null':
            index = index + 1
            createtrihoImage(enfermedadtriho.id, index, image)

    return enfermedadtriho.id


def createtrihoImage(id, index, image):
    imgCore = image.split(',')[1]
    imgFile = open(settings.ENFERMEDADTRIHO_IMAGEN_DIR + "/" + str(id) + "_" + str(index) + ".jpeg", "wb")
    imgFile.write(imgCore.decode('base64'))
    imgFile.close()

   
    img = Image.open(settings.ENFERMEDADTRIHO_IMAGEN_DIR + "/" + str(id) + "_" + str(index) + ".jpeg")
    longer_side = max(img.size)
    thumb = Image.new('RGBA', (longer_side, longer_side), (255, 255, 255, 0))
    thumb.paste(
        img, ((longer_side - img.size[0]) / 2, (longer_side - img.size[1]) / 2)
    )
    thumb.save(settings.ENFERMEDADTRIHO_IMAGEN_DIR + "/" + str(id) + "_" + str(index) + "_square.jpeg")


@csrf_exempt
def escrituratrihoPage(request):
    enfermedadtrihomaiz = Enfermedadtriho.objects.latest('id')
    return render(request, 'escrituratriho.html', {'enfermedadtrihomaiz':enfermedadtrihomaiz})       


@csrf_exempt
def escrituratriho(request):
  
  if request.method == "POST":
    insetarEscrituratrihoSE()
    return render(request, 'escrituratriho.html')


# INICIO NUEVO BONJOUR---------

def insetarEscrituratrihoSE():
    FactsFile = settings.CLIPS_DIR + "/enfermedadestriho.clp"
    if not os.path.isfile(FactsFile):
        file = open(FactsFile, 'w+')
        file.write("(deffacts enfermedades)\n")
        file.close()

    #nuevalinea
    suggestions = Enfermedadtriho.objects.all()
    #finnuevalinea
    lines = ['(deffacts enfermedades\n']
    for suggestion in suggestions:
        lines.append('    (enfermedad '
                        '(ID '+str(suggestion.id)+')'
                        '(name "'+str(suggestion.name)+'") '
                        '(planta "'+str(suggestion.planta)+'") '
                        '(sintoma-aa "'+str(suggestion.sintomaAA)+'") '
                        '(sintoma-bb "'+str(suggestion.sintomaBB)+'") '
                        '(sintoma-cc "'+str(suggestion.sintomaCC)+'") '
                        '(stars -1))\n')

    lines.append(')\n')

    # new facts
#    open(FactsFile, 'w').writelines(lines)  
    open(FactsFile, 'w').writelines(lines)   

# FIN NUEVO BONJOUR----------


@login_required
def reportetrihomaizPage(request):
    enfermedadtrihomaiz = Enfermedadtriho.objects.all()
    return render(request, 'reportetrihomaiz.html', {'enfermedadtrihomaiz':enfermedadtrihomaiz})


@login_required
def reportecalificacionmaiztrihoPage(request):
    reviewmaiz = Reviewtriho.objects.order_by('-stars')
    return render(request, 'reportecalificacionmaiztriho.html', {'reviewmaiz':reviewmaiz})


@login_required
def accionestrihoPage(request):
    enfermedadtrihomaiz = Enfermedadtriho.objects.all()
    return render(request, 'accionestriho.html', {'enfermedadtrihomaiz':enfermedadtrihomaiz}) 


#inicio cf

def enfermedadtrihomaiz_view(request):
    if request.method == 'POST':
        form = EnfermedadtrihomaizForm(request.POST) 
        if form.is_valid():
            form.save()
        return redirect('enfermedadtrihomaiz:index')
    else:
        form = EnfermedadtrihomaizForm()
    return render(request, 'enfermedadtrihomaiz_form.html', {'form':form})  


def enfermedadtrihomaiz_edit(request,id_enfermedadtrihomaiz):
    enfermedadtrihomaiz = Enfermedadtriho.objects.get(id=id_enfermedadtrihomaiz)     
    if request.method == 'GET':
        form = EnfermedadtrihomaizForm(instance=enfermedadtrihomaiz)
    else:
        form = EnfermedadtrihomaizForm(request.POST, instance=enfermedadtrihomaiz)
        if form.is_valid():
            form.save()
        return redirect('accionestrihoPage')
    return render(request, 'enfermedadtrihomaiz_form.html', {'form':form}) 


def enfermedadtrihomaiz_delete(request, id_enfermedadtrihomaiz):
    enfermedadtrihomaiz = Enfermedadtriho.objects.get(id=id_enfermedadtrihomaiz)
    if request.method == 'POST':
        enfermedadtrihomaiz.delete()
        return redirect('accionestrihoPage')
    return render(request,'enfermedadtrihomaiz_delete.html', {'enfermedadtrihomaiz':enfermedadtrihomaiz}) 

#fin cf

#TRIPLA-------------------------------------------------------------------------

def analisistriplaPagina(request):
    return render(request, 'analisistripla.html')  


@csrf_exempt
def agregarAnalisistripla(request):
    result = seInferAnalisistripla(request.POST)
    print(result)
    response = []
    if result != None:
        for val in result.split('---'):
            if "," in val:
                val2 = val.split(',')
                enfermedadtripla = Enfermedadtripla.objects.get(id=int(val2[0]))
                response.append({"id": enfermedadtripla.id, "name": enfermedadtripla.name, "images": enfermedadtripla.images, "description": enfermedadtripla.description,
                    "planta": val2[1], "sintomaAAA": val2[2], "sintomaBB": val2[3], 
                    "sintomaCC": val2[4], "sintomaDD": val2[5], "sintomaEE": val2[6],
                    "stars": float(val2[7])})

    return JsonResponse(response, safe=False) 


def seInferAnalisistripla(data):
    
    analisis = '(analisis ' +\
                 '(planta "'+data['planta']+'") ' +\
                 '(sintoma-aa "'+data['sintomaAA']+'") ' +\
                 '(sintoma-bb "'+data['sintomaBB']+'") ' +\
                 '(sintoma-cc "'+data['sintomaCC']+'") ' +\
                 '(sintoma-ee "'+data['sintomaEE']+'") ' +\
                 '(sintoma-dd "'+data['sintomaDD']+'"))'

    
    clips.Clear()
    clips.BatchStar(settings.CLIPS_DIR + "/templatestripla.clp")
    if os.path.isfile(settings.CLIPS_DIR + "/enfermedadestripla.clp"):
        clips.BatchStar(settings.CLIPS_DIR + "/enfermedadestripla.clp")
    if os.path.isfile(settings.XTRAS_DIR + "/calificacionestripla.clp"):
        clips.BatchStar(settings.XTRAS_DIR + "/calificacionestripla.clp")
    clips.BatchStar(settings.CLIPS_DIR + "/reglastripla.clp")
    clips.Reset()
    clips.Assert(analisis)
    clips.Run()
    return clips.StdoutStream.Read()



@csrf_exempt
def procesarCalificaciontripla(request):
    if request.method == "POST":
        id = insertarCalificaciontriplaBD(request.POST)
        insertarCalificaciontriplaSE(request.POST, id)
        return HttpResponse('')
    else:
        response = []
        reviews = Reviewtripla.objects.filter(enfermedadId=int(request.GET['enfermedadId'])).order_by("-id")
        for review in reviews:
            response.append({"id": review.id, "comment": review.comment, "reviewer": review.reviewer,
                    "createdTime": review.createdTime})
        return JsonResponse(response, safe=False)


def insertarCalificaciontriplaBD(data):
    review = Reviewtripla(reviewer=data['reviewer'],
                comment=data['comment'],
                stars=float(data['stars']),
                enfermedadName=data['enfermedadName'],
                enfermedadId=int(data['enfermedadId']),
                createdTime=datetime.datetime.now())
    print(review)
    review.save()
    return review.id


def insertarCalificaciontriplaSE(data, id):
    
    FactsFile = settings.XTRAS_DIR + "/calificacionestripla.clp"
    if not os.path.isfile(FactsFile):
        file = open(FactsFile, 'w+')
        file.write("(deffacts reviews)\n")
        file.close()

    
    lines = open(FactsFile, 'r+').readlines()
    n = len(lines)
    lines[n - 1] = lines[n-1][:-2] + "\n"
    lines.append('  (review '
                '(ID '+str(id)+')'
                '(enfermedad-name "'+data['enfermedadName']+'")'
                '(enfermedad-id '+data['enfermedadId']+')'
                '(reviewer "'+data['reviewer']+'")'
                '(comment "'+data['comment']+'")'
                '(stars '+data['stars']+')))\n')

    
    open(FactsFile, 'w').writelines(lines)


@login_required
def nuevotriplaEnfermedadPagina(request):
    return render(request, 'agregartripla.html')  



@csrf_exempt
def creartriplaEnfermedad(request):
    id = insertartriplaNuevaEnfermedad(request.POST)

    return HttpResponse('')



def insertartriplaNuevaEnfermedad(data):
    images = ast.literal_eval(data['images'])
    imageNum = 0;
    for image in images:
        imageNum = imageNum + (image != 'null')

    enfermedadtripla = Enfermedadtripla(name=data['name'],
                description=data['description'],
                images=imageNum,
                planta=data['planta'],
                sintomaAA=data['sintomaAA'],
                sintomaBB=data['sintomaBB'],
                sintomaCC=data['sintomaCC'],
                sintomaEE=data['sintomaEE'],
                sintomaDD=data['sintomaDD'])
    enfermedadtripla.save()

    index = 0
    for image in images:
        if image != 'null':
            index = index + 1
            createtriplaImage(enfermedadtripla.id, index, image)

    return enfermedadtripla.id


def createtriplaImage(id, index, image):
    imgCore = image.split(',')[1]
    imgFile = open(settings.ENFERMEDADTRIPLA_IMAGEN_DIR + "/" + str(id) + "_" + str(index) + ".jpeg", "wb")
    imgFile.write(imgCore.decode('base64'))
    imgFile.close()


    img = Image.open(settings.ENFERMEDADTRIPLA_IMAGEN_DIR + "/" + str(id) + "_" + str(index) + ".jpeg")
    longer_side = max(img.size)
    thumb = Image.new('RGBA', (longer_side, longer_side), (255, 255, 255, 0))
    thumb.paste(
        img, ((longer_side - img.size[0]) / 2, (longer_side - img.size[1]) / 2)
    )
    thumb.save(settings.ENFERMEDADTRIPLA_IMAGEN_DIR + "/" + str(id) + "_" + str(index) + "_square.jpeg")   


@csrf_exempt
def escrituratriplaPage(request):
    enfermedadtriplamaiz = Enfermedadtripla.objects.latest('id')
    return render(request, 'escrituratripla.html', {'enfermedadtriplamaiz':enfermedadtriplamaiz})  


@csrf_exempt
def escrituratripla(request):
  if request.method == "POST":
    insetarEscrituratriplaSE()
    return render(request, 'escrituratripla.html')


# INICIO NUEVO BONJOUR---------

def insetarEscrituratriplaSE():
    FactsFile = settings.CLIPS_DIR + "/enfermedadestripla.clp"
    if not os.path.isfile(FactsFile):
        file = open(FactsFile, 'w+')
        file.write("(deffacts enfermedades)\n")
        file.close()

    #nuevalinea
    suggestions = Enfermedadtripla.objects.all()
    #finnuevalinea
    lines = ['(deffacts enfermedades\n']
    for suggestion in suggestions:
        lines.append('    (enfermedad '
                        '(ID '+str(suggestion.id)+')'
                        '(name "'+str(suggestion.name)+'") '
                        '(planta "'+str(suggestion.planta)+'") '
                        '(sintoma-aa "'+str(suggestion.sintomaAA)+'") '
                        '(sintoma-bb "'+str(suggestion.sintomaBB)+'") '
                        '(sintoma-cc "'+str(suggestion.sintomaCC)+'") '
                        '(sintoma-dd "'+str(suggestion.sintomaDD)+'") '
                        '(sintoma-ee "'+str(suggestion.sintomaEE)+'") '
                        '(stars -1))\n')

    lines.append(')\n')

    # new facts
#    open(FactsFile, 'w').writelines(lines)  
    open(FactsFile, 'w').writelines(lines)   

# FIN NUEVO BONJOUR----------


@login_required
def reportetriplamaizPage(request):
    enfermedadtriplamaiz = Enfermedadtripla.objects.all()
    return render(request, 'reportetriplamaiz.html', {'enfermedadtriplamaiz':enfermedadtriplamaiz})


@login_required
def reportecalificacionmaiztriplaPage(request):
    reviewmaiz = Reviewtripla.objects.order_by('-stars')
    return render(request, 'reportecalificacionmaiztripla.html', {'reviewmaiz':reviewmaiz})


@login_required
def accionestriplaPage(request):
    enfermedadtriplamaiz = Enfermedadtripla.objects.all()
    return render(request, 'accionestripla.html', {'enfermedadtriplamaiz':enfermedadtriplamaiz})


#inicio cf

def enfermedadtriplamaiz_view(request):
    if request.method == 'POST':
        form = EnfermedadtriplamaizForm(request.POST) 
        if form.is_valid():
            form.save()
        return redirect('enfermedadtriplamaiz:index')
    else:
        form = EnfermedadtriplamaizForm()
    return render(request, 'enfermedadtriplamaiz_form.html', {'form':form})  


def enfermedadtriplamaiz_edit(request,id_enfermedadtriplamaiz):
    enfermedadtriplamaiz = Enfermedadtripla.objects.get(id=id_enfermedadtriplamaiz)     
    if request.method == 'GET':
        form = EnfermedadtriplamaizForm(instance=enfermedadtriplamaiz)
    else:
        form = EnfermedadtriplamaizForm(request.POST, instance=enfermedadtriplamaiz)
        if form.is_valid():
            form.save()
        return redirect('accionestriplaPage')
    return render(request, 'enfermedadtriplamaiz_form.html', {'form':form}) 


def enfermedadtriplamaiz_delete(request, id_enfermedadtriplamaiz):
    enfermedadtriplamaiz = Enfermedadtripla.objects.get(id=id_enfermedadtriplamaiz)
    if request.method == 'POST':
        enfermedadtriplamaiz.delete()
        return redirect('accionestriplaPage')
    return render(request,'enfermedadtriplamaiz_delete.html', {'enfermedadtriplamaiz':enfermedadtriplamaiz}) 

#fin cf