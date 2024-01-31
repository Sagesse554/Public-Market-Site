import json
from django.shortcuts import render, redirect
from datetime import datetime, date
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import View
from appels.models import Appel_d_Offre
from projets.models import Projet_d_Approvisionnement, Etape1
from projets.forms import ProjectForm, Step1Form


class ProjetView(LoginRequiredMixin, View):
    template_name = 'project.html'
    
    def get(self, request):
        if request.user.Ent_numero.Ent_numero.Rgs_numero == '1613978901' and request.GET.get('pjt') is not None:
            pjt = Projet_d_Approvisionnement.objects.get(Pjt_numero=request.GET.get('pjt'))
            if pjt is not None:
                pjt.appel_count = Appel_d_Offre.objects.filter(Pjt_numero=pjt).count()
                pjt.etapes = Etape1.objects.filter(Pjt_numero=pjt)
                context = {'pjt' : pjt}
                return render(request, self.template_name, context)
            else:
                return redirect('projets')
        elif request.GET.get('pjt') is None:
            return redirect('projets')
        else:
            return redirect(f"{reverse('signin')}?next=/projet?pjt={pjt}/")


class ProjetsView(LoginRequiredMixin, View):
    template_name = 'projets.html'
    
    def get(self, request):
        if request.user.Ent_numero.Ent_numero.Rgs_numero == '1613978901':
            context = {}
            pjt = Projet_d_Approvisionnement.objects.filter(Pjt_statut='EN_COURS')
            for pj in pjt:
                pj.appel_count = Appel_d_Offre.objects.filter(Pjt_numero=pj).count()
            pjtn = pjt.count()
            if pjtn != 0:
                context['pjt'] = pjt
                context['pjtn'] = pjtn
            else:
                context['pjtn'] = pjtn
            return render(request, self.template_name, context)
        else:
            return redirect(f"{reverse('signin')}?next=/projets/")


class ProjectView(LoginRequiredMixin, View):
    template_name = 'projet.html'
    form_class = ProjectForm
    #formset_class = Step1Form
    #display_name = {
        #'Etp1_titre' : 'Titre',
        #'Etp1_dateDebut' : 'Date de Début',
        #'Etp1_dateFin' : 'Date de Fin',
        #'Etp1_description' : 'Description',
        #'Etp1_objectifs' : 'Objectifs',
        #'Etp1_budget' : 'Budget',
    #}
    
    def get(self, request):
        if request.user.Ent_numero.Ent_numero.Rgs_numero == '1613978901':
            form = self.form_class()
            #formset = self.formset_class()
            #if request.POST.get('num') is not None:
                #num = int(request.POST.get('num'))
                #formset_data = str(request.POST.get('formset_data'))[2:-2]
                #formset_data = formset_data.split('}, {')
                #formset_data3 = []
                #for data in formset_data:
                    #data = data.replace('\'', '"')
                    #data = '{'+data+'}'
                    #formset_data3 += [json.loads(data)]
                #formset_data = formset_data3
            #else :
                #num = 1
                #formset_data = []
            #context = {'form' : form, 'formset': formset, 'num' : num, 'formset_data' : formset_data, 'display_name' : self.display_name}
            context = {'form' : form}
            return render(request, self.template_name, context)
        else:
            return redirect(f"{reverse('signin')}?next=/project/")

    def post(self, request):
        """if request.POST.get('num') is not None:
            num = int(request.POST.get('num'))
            formset_data = str(request.POST.get('formset_data'))[2:-2]
            formset_data = formset_data.split('}, {')
            formset_data3 = []
            for data in formset_data:
                data = data.replace('\'', '"')
                data = '{'+data+'}'
                formset_data3 += [json.loads(data)]
            formset_data = formset_data3
        else :
            num = 1
            formset_data = []
        form = self.form_class(data=request.POST)
        formset = self.formset_class(data=request.POST)"""
        
        #if form.is_valid() and formset.is_valid():
        if form.is_valid():
            
            """if 'remove' in request.POST:
                num -= 1
                rid = int(request.POST.get('rid'))
                formset_data.remove(formset_data[rid-1])
                context = {'form': form, 'formset': formset, 'num': num, 'formset_data' : formset_data, 'display_name' : self.display_name}
                return render(request, self.template_name, context)
            
            else:"""
            #project_data = form.cleaned_data
            #formset_data = formset_data[1:]
            #formset_data2 = formset_data
            #cleaned_data = formset.cleaned_data
            #formset_data2 += [cleaned_data]
            #budgetsum = 0
            
            """for step1_data in formset_data2:
                print(step1_data)
                budgetsum += step1_data['Etp1_budget']
            
                if step1_data['Etp1_dateDebut'] < project_data['Pjt_dateDebut']:
                    print('Project registration 1-failed!')
                    formset.add_error('Etp1_dateDebut', 'Respectez les limites du projet !')
                    return render(request, self.template_name, {'form': form, 'formset': formset, 'num' : num, 'formset_data' : formset_data, 'display_name' : self.display_name})                
                        
                elif project_data['Pjt_dateFin'] < step1_data['Etp1_dateFin']:
                    print('Project registration 2-failed!')
                    formset.add_error('Etp1_dateFin', 'Respectez les limites du projet !')
                    return render(request, self.template_name, {'form': form, 'formset': formset, 'num' : num, 'formset_data' : formset_data, 'display_name' : self.display_name}) 

                elif project_data['Pjt_budget'] <= budgetsum:
                    print('Project registration 3-failed!')
                    form.add_error('Pjt_budget', 'La somme des budgets d\'étape ne peut dépasser le budget de projet !')
                    return render(request, self.template_name, {'form': form, 'formset': formset, 'num' : num, 'formset_data' : formset_data, 'display_name' : self.display_name})
                
                elif 'add' in request.POST:
                    num += 1
                    formset_data += [cleaned_data]
                    formset = self.formset_class()
                    context = {'form': form, 'formset': formset, 'num': num, 'formset_data' : formset_data, 'display_name' : self.display_name}
                    return render(request, self.template_name, context)
        
                elif num == 1:
                    num += 1    
                    formset.add_error('Etp1_statut', 'La programmation du projet avec chacune de ses étapes est importante !')
                    formset_data += [cleaned_data]
                    formset = self.formset_class()
                    context = {'form': form, 'formset': formset, 'num' : num, 'formset_data' : formset_data, 'display_name' : self.display_name}
                return render(request, self.template_name, context)"""
            
            project = form.save()
            
            """for step1_data in formset_data2:
                step1_data['Pjt_numero'] = project
                Etape1.objects.create(**step1_data)"""
            
            print("Project registration successful!")
            return redirect("home")
    
        else:
            print('Project registration 4-failed!')
            return render(request, self.template_name, {'form': form})
            #return render(request, self.template_name, {'form': form, 'formset': formset, 'num' : num, 'formset_data' : formset_data, 'display_name' : self.display_name})