from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from appels.forms import CallManifestForm, CallOfferForm, Service1Form, CategoryForm, CriteriaForm
from appels.models import Appel_d_Offre, Appel_a_Manifestation
from entreprises.models import Manifestation
from reponses.models import Offre
from projets.models import Projet_d_Approvisionnement


class ManifCallView(View):
    template_name = 'manifcall.html'
    
    def get(self, request):
        if request.GET.get('ami') is not None:
            ami = Appel_a_Manifestation.objects.get(Ami_numero=request.GET.get('ami'))
            if ami is not None:
                ami.entreprise_count = Manifestation.objects.filter(Ami_numero=ami).count()
                return render(request, self.template_name, {'ami' : ami})
            else:
                return redirect("manifestcall")
        else:
            return redirect("manifestcall")


class OffCallView(View):
    template_name = 'offcall.html'
    
    def get(self, request):
        if request.GET.get('apl') is not None:
            apl = Appel_d_Offre.objects.get(Apl_numero=request.GET.get('apl'))
            if apl is not None:
                apl.offre_count = Offre.objects.filter(Apl_numero=apl).count()
                return render(request, self.template_name, {'apl' : apl})
            else:
                return redirect("offercall")
        else:
            return redirect("offercall")


class ManifestCallView(View):
    template_name = 'manifestcall.html'
    
    def get(self, request):
        amic = Appel_a_Manifestation.objects.filter(Ami_statut='EN_COURS')
        for ami in amic:
            ami.entreprise_count = Manifestation.objects.filter(Ami_numero=ami).count()
        amicn = amic.count()
        return render(request, self.template_name, {'amic' : amic, 'amicn' : amicn})


class OfferCallView(View):
    template_name = 'offercall.html'
    
    def get(self, request):
        request.GET.get('pjt')
        if pjt is not None:
            aplc = Appel_d_Offre.objects.filter(Pjt_numero=pjt)
        else:
            aplc = Appel_d_Offre.objects.filter(Apl_statut='EN_COURS')
        for apl in aplc:
            apl.offre_count = Offre.objects.filter(Apl_numero=apl).count()
        aplcn = aplc.count()
        context = {'aplc' : aplc, 'aplcn' : aplcn}
        if request.GET.get('pjt') is not None:
            context['pjt'] = pjt
        return render(request, self.template_name, context)


class CallManifestView(LoginRequiredMixin, View):
    template_name = 'callmanifest.html'
    form_class = CallManifestForm

    def get(self, request):
        if request.user.Ent_numero.Ent_numero.Rgs_numero == '1613978901':
            form = self.form_class()
            return render(request, self.template_name, {'form' : form})
        else:
            return redirect(f"{reverse('signin')}?next=/callmanifest/")
            

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            manifestcall = form.save()
            print("Manifestation Call registered !")
            return redirect("home")

        else:
            print(form, "Manifestation Call not registered !")
            return render(request, self.template_name, {'form': form})


class CallOfferView(LoginRequiredMixin, View):
    template_name = 'calloffer.html'
    form_class = CallOfferForm
    form_class1 = Service1Form
    form_class2 = CategoryForm
    form_class3 = CriteriaForm

    def get(self, request):
        if request.user.Ent_numero.Ent_numero.Rgs_numero == '1613978901':    
            form = self.form_class()
            form1 = self.form_class1()
            form2 = self.form_class2()
            form3 = self.form_class3()
            pjt = request.GET.get('pjt')
            if pjt is not None:
                context = {'form': form, 'form1': form1, 'form2' : form2, 'form3': form3, 'pjt' : pjt}
                return render(request, self.template_name, context)
            else:
                return redirect("projets")
        else:
            return redirect(f"{reverse('signin')}?next=/calloffer/")

    def post(self, request):

        if 'button' in request.POST:
            form = self.form_class(request.POST, request.FILES)

            if form.is_valid():
                pjt = request.POST.get('pjt')
                offer_data = form.cleaned_data
                offer_data['Pjt_numero'] = pjt
                prestations = offer_data.pop('Apl_prestations')
                criteres = offer_data.pop('Apl_criteres')
                offercall = Appel_d_Offre(**offer_data)
                offercall.save()
                for prestation in prestations:
                    offercall.Apl_prestations.add(prestation)
                for critere in criteres:
                    offercall.Apl_criteres.add(critere)
                print("Offer Call registered !")
                return redirect("home")

            else:
                print("Offer Call not registered !")
                pjt = request.POST.get('pjt')
                context = {'form': form, 'form1': Service1Form(), 'form2' : CategoryForm(), 'form3': CriteriaForm(), 'pjt' : pjt}
                return render(request, self.template_name, context)

        elif 'button1' in request.POST:
            form1 = self.form_class1(request.POST)

            if form1.is_valid():
                service1 = form1.save()
                print("Service registered !")
                pjt = request.POST.get('pjt')
                context = {'form': CallOfferForm(), 'form1': Service1Form(), 'form2' : CategoryForm(), 'form3': CriteriaForm(), 'pjt' : pjt}
                return render(request, self.template_name, context)

            else:
                print("Service not registered !")
                pjt = request.POST.get('pjt')
                context = {'form': CallOfferForm(), 'form1': form1, 'form2' : CategoryForm(), 'form3': CriteriaForm(), 'pjt' : pjt}
                return render(request, self.template_name, context)

        elif 'button2' in request.POST:
            form2 = self.form_class2(request.POST)

            if form2.is_valid():
                category = form2.save()
                print("Category registered !")
                pjt = request.POST.get('pjt')
                context = {'form': CallOfferForm(), 'form1': Service1Form(), 'form2' : CategoryForm(), 'form3': CriteriaForm(), 'pjt' : pjt}
                return render(request, self.template_name, context)

            else:
                print("Category not registered !")
                pjt = request.POST.get('pjt')
                context = {'form': CallOfferForm(), 'form1': Service1Form(), 'form2' : form2, 'form3': CriteriaForm(), 'pjt' : pjt}
                return render(request, self.template_name, context)

        elif 'button3' in request.POST:
            form3 = self.form_class3(request.POST)

            if form3.is_valid():
                criteria = form3.save()
                print("Criteria registered !")
                pjt = request.POST.get('pjt')
                context = {'form': CallOfferForm(), 'form1': Service1Form(), 'form2' : CategoryForm(), 'form3': CriteriaForm(), 'pjt' : pjt}
                return render(request, self.template_name, context)

            else:
                print("Criteria not registered !")
                pjt = request.POST.get('pjt')
                context = {'form': CallOfferForm(), 'form1': Service1Form(), 'form2' : CategoryForm(), 'form3': form3, 'pjt' : pjt}
                return render(request, self.template_name, context)            