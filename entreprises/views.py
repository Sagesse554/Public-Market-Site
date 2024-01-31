from datetime import timedelta
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.db.models import Q, Max
from django.views import View
from entreprises.models import Entreprise, Manifestation, Reference, Allocation1, Allocation2
from entreprises.forms import EnterpriseForm, ManifestForm, ReferenceForm, Service3FormSet, Service2Form, EquipmentFormSet, StaffFormSet, EquipmentForm, StaffForm
from appels.forms import CategoryForm


class EntrepriseView(LoginRequiredMixin, View):
    template_name = 'entreprise.html'
    
    def get(self, request):
        context = {}
        ent = request.user.Ent_numero
        if ent.Ent_numero.Rgs_numero != '1613978901':
            last_mnf_moment = Manifestation.objects.filter(Ent_numero=ent).aggregate(last_mnf_moment=Max('Mnf_moment'))['last_mnf_moment']
            mnf = Manifestation.objects.get(Q(Ent_numero=ent) & Q(Mnf_moment=last_mnf_moment))
            ent.manif = mnf
            ent.references = Reference.objects.filter(Ent_numero=ent)
            ent.personnel = Allocation1.objects.filter(Mnf_id=mnf)
            ent.materiel = Allocation2.objects.filter(Mnf_id=mnf)
        elif request.GET.get('ent') is not None:
            ent = request.GET.get('ent')
            last_mnf_moment = Manifestation.objects.filter(Ent_numero=ent).aggregate(last_mnf_moment=Max('Mnf_moment'))['last_mnf_moment']
            mnf = Manifestation.objects.get(Q(Ent_numero=ent) & Q(Mnf_moment=last_mnf_moment))
            ent.manif = mnf
            ent.references = Reference.objects.filter(Ent_numero=ent)
            ent.personnel = Allocation1.objects.filter(Mnf_id=mnf)
            ent.materiel = Allocation2.objects.filter(Mnf_id=mnf)
        context['ent'] = ent
        return render(request, self.template_name, context)


class EntreprisesView(LoginRequiredMixin, View):
    template_name = 'entreprises.html'
    
    def get(self, request):
        if request.user.Ent_numero.Ent_numero.Rgs_numero == '1613978901':
            context = {}
            if request.GET.get('ami') is not None:
                mnfs, entv, mnfv = Manifestation.objects.filter(Q(Ent_numero.Ent_numero.Rgs_numero!='1613978901') & Q(Ami_numero=ami)), [], []
            else:
                mnfs, entv, mnfv = Manifestation.objects.filter(Ent_numero.Ent_numero.Rgs_numero!='1613978901'), [], []
            for mnf in mnfs:
                mnf.date_limite = mnf.Ami_numero.Ami_dateFin + timedelta(mnf.Ami_numero.Ami_delaiValidite)
                if mnf.date_limite >= timezone.now().date():
                    entv.append(mnf.Ent_numero.Ent_numero.Rgs_numero)
                    mnfv.append(mnf.Mnf_id)
            ents = Entreprise.objects.filter(Ent_numero__Rgs_numero__in=entv)
            for ent in ents:
                last_mnf_moment = Manifestation.objects.filter(Q(Ent_numero=ent) & Q(Mnf_id__in=mnfv)).aggregate(last_mnf_moment=Max('Mnf_moment'))['last_mnf_moment']
                mnf = Manifestation.objects.get(Q(Ent_numero=ent) & Q(Mnf_moment=last_mnf_moment))
                ent.manif = mnf
            entsn = ents.count()
            if entsn != 0:
                context['ents'] = ents
                context['entsn'] = entsn
            else:
                context['entsn'] = entsn
            if request.GET.get('ami') is not None:
                context['ami'] = ami
            return render(request, self.template_name, context)
        else:
            return redirect(f"{reverse('signin')}?next=/entreprises/")


class ManifestView(View):
    template_name = 'manifest.html'
    form_class1 = EnterpriseForm
    form_class2 = ManifestForm

    def get(self, request):
        if request.user.is_authenticated:
            if request.user.Ent_numero.Ent_numero.Rgs_numero != '1613978901':
                form1 = self.form_class1()
                form2 = self.form_class2()
                ami = request.POST.get('ami')
                if ami is not None:
                    amio = Appel_a_Manifestation.objects.get(Ami_numero=ami)
                    if amio is not None:
                        context = {'form1': form1, 'form2' : form2, 'ami' : ami}
                        return render(request, self.template_name, context)
                    else:                 
                        return redirect('manifestcall')   
                else:
                    return redirect('manifestcall')
            else:
                return redirect(f"{reverse('signin')}?next=/manifest/")
        else:
            form1 = self.form_class1()
            form2 = self.form_class2()
            ami = request.POST.get('ami')
            if ami is not None:
                context = {'form1': form1, 'form2' : form2, 'ami' : ami}
                return render(request, self.template_name, context)
            else:
                return redirect('manifestcall')

    def post(self, request):
        form1 = self.form_class1(request.POST)
        form2 = self.form_class2(request.POST, request.FILES)

        if form1.is_valid() and form2.is_valid():
            enterprise = form1.save()
            
            ami = request.GET.get('ami')
            manifest_data = form2.cleaned_data
            manifest_data['Ami_numero'] = ami
            manifest_data['Ent_numero'] = enterprise
            manifest = Manifestation.objects.create(**manifest_data)
            
            print("Enterprise registered successfully!")
            
            return redirect("home")

        else:
            print("Enterprise registration failed!")
            ami = request.GET.get('ami')
            context = {'form1': form1, 'form2' : form2, 'ami' : ami}
            return render(request, self.template_name, context)


class ReferenceView(LoginRequiredMixin, View):
    template_name = 'reference.html'
    form_class1 = ReferenceForm
    #formset_class = Service3FormSet
    form_class2 = CategoryForm

    def get(self, request):
        if request.user.Ent_numero.Ent_numero.Rgs_numero != '1613978901':
            ent = request.GET.get('ent')
            mnf = request.GET.get('mnf')
            if ent is not None and mnf is not None:
                mnf = int(mnf)
                ent = Entreprise.objects.get(Ent_numero__Rgs_numero=ent)
                mnf = Manifestation.objects.get(Mnf_id=mnf)
                if mnf is not None and ent is not None:
                    form1 = self.form_class1()
                    #formset = self.formset_class()
                    form2 = self.form_class2()
                    context = {'form1': form1, 'form2' : form2, 'ent' : ent, 'mnf' : mnf}
                    #context = {'form1': form1, 'formset': formset, 'form2' : form2, 'ent' : ent, 'mnf' : mnf}
                    return render(request, self.template_name, context)
                else:
                    return redirect('home')   
            else:
                return redirect('home')
        else:
            return redirect("home")

    def post(self, request):        
        ent = request.POST.get('ent')
        mnf = request.POST.get('mnf')

        """if 'add' in request.POST:
            form1 = self.form_class1(request.POST, request.FILES)
            formset = self.formset_class(request.POST)
            formset.forms.append(formset.empty_form)
            context = {'form1': form1, 'formset': formset, 'form2': CategoryForm(), 'ent': ent, 'mnf' : mnf}
            return render(request, self.template_name, context)
            
        elif 'remove' in request.POST:
            form1 = self.form_class1(request.POST, request.FILES)
            formset = self.formset_class(request.POST, reference_form=form1)
            form_index = int(request.POST.get('delete'))
            formset.forms[form_index].delete()
            context = {'form1': form1, 'formset': formset, 'form2': CategoryForm(), 'ent': ent, 'mnf' : mnf}
            return render(request, self.template_name, context)"""

        #elif 'button1' in request.POST:
        if 'button1' in request.POST:
            form1 = self.form_class1(request.POST, request.FILES)
            #formset = self.formset_class(request.POST)

            if form1.is_valid() and formset.is_valid():
                ent = request.POST.get('ent')
                reference_data = form1.cleaned_data
                reference_data['Ent_numero'] = ent
                categories = reference_data.pop('Rfc_categories')
                reference = Reference(**reference_data)
                reference.save()
                for categorie in categories:
                    reference.Rfc_categories.add(categorie)

                for form_service3 in formset:
                    service3_data = form_service3.cleaned_data
                    service3_data['Rfc_id'] = reference
                    Prestation3.objects.create(**service3_data)

                print("Reference registration successful !")
                return redirect(f"{reverse('service')}?mnf={mnf}")
            
            else:
                print("Reference registration failed !")
                context = {'form1': form1, 'formset': formset, 'form2' : CategoryForm(), 'ent' : ent, 'mnf' : mnf}
                return render(request, self.template_name, context)
            
        elif 'button2' in request.POST:
            form2 = self.form_class2(request.POST)

            if form2.is_valid():
                category = form2.save()
                print("Category registered !")    
                context = {'form1': ReferenceForm(), 'formset': Service3FormSet(), 'form2' : CategoryForm(), 'ent' : ent, 'mnf' : mnf}
                return render(request, self.template_name, context)
            
            else:
                print("Category registered !")
                context = {'form1': ReferenceForm(), 'formset': Service3FormSet(), 'form2' : form2, 'ent' : ent, 'mnf' : mnf}
                return render(request, self.template_name, context)
            


class Service2View(LoginRequiredMixin, View):
    template_name = 'service.html'
    form_class =   Service2Form
    formset_class1 = EquipmentFormSet
    formset_class2 = StaffFormSet
    form_class1 = CategoryForm
    form_class2 = EquipmentForm
    form_class3 = StaffForm

    def get(self, request):
        if request.user.Ent_numero.Ent_numero.Rgs_numero != '1613978901':
            mnf = request.GET.get('mnf')
            if mnf is not None:            
                mnf = int(mnf)
                mnf = Manifestation.objects.get(Mnf_id=mnf)
                if mnf is not None:
                    form = self.form_class()
                    formset1 = self.formset_class1()
                    formset2 = self.formset_class2()
                    form1 = self.form_class1()
                    form2 = self.form_class2()
                    form3 = self.form_class3()
                    context = {'form': form, 'formset1': formset1, 'formset2': formset2, 'form1' : form1, 'form2' : form2, 'form3' : form3, 'mnf' : mnf}
                    return render(request, self.template_name, context)
                else:
                    return redirect("home")                
            else:
                return redirect("home")
        else:
            return redirect("home")

    def post(self, request):      
        mnf = request.POST.get('mnf')
        mnf = int(mnf)

        if 'button' in request.POST:
            form = self.form_class(request.POST)
            formset1 = self.formset_class1(request.POST)
            formset2 = self.formset_class2(request.POST)

            if form.is_valid() and formset1.is_valid() and formset2.is_valid():
                service2 = form.save()

                for form_equipment in formset1:
                    equipment_data = form_equipment.cleaned_data
                    equipment_data['Mnf_id'] = mnf
                    equipment_data['Ptn2_id'] = service2
                    Allocation2.objects.create(**equipment_data)

                for form_staff in formset2:
                    staff_data = form_staff.cleaned_data
                    staff_data['Mnf_id'] = mnf
                    staff_data['Ptn2_id'] = service2
                    Allocation1.objects.create(**staff_data)

                print("Service registration successful !")
                return redirect('home')
            
            else:
                print("Service registration failed !")
                context = {'form': form, 'formset1': formset1, 'formset2': formset2, 'form1' : CategoryForm(), 'form2' : EquipmentForm(), 'form3' : StaffForm(), 'mnf' : mnf}
                return render(request, self.template_name, context)
            
        elif 'button1' in request.POST:
            form1 = self.form_class1(request.POST)

            if form1.is_valid():
                category = form1.save()
                print("Category registered !")
                context = {'form': Service2Form(), 'formset1': EquipmentFormSet(), 'formset2': StaffFormSet(), 'form1' : CategoryForm(), 'form2' : EquipmentForm(), 'form3' : StaffForm(), 'mnf' : mnf}
                return render(request, self.template_name, context)
            
            else:
                print("Category not registered !")
                context = {'form': Service2Form(), 'formset1': EquipmentFormSet(), 'formset2': StaffFormSet(), 'form1' : form1, 'form2' : EquipmentForm(), 'form3' : StaffForm(), 'mnf' : mnf}
                return render(request, self.template_name, context)

        elif 'button2' in request.POST:
            form2 = self.form_class2(request.POST)

            if form1.is_valid():    
                equipment = form2.save()
                print("Equipment registered !")
                context = {'form': Service2Form(), 'formset1': EquipmentFormSet(), 'formset2': StaffFormSet(), 'form1' : CategoryForm(), 'form2' : EquipmentForm(), 'form3' : StaffForm(), 'mnf' : mnf}
                return render(request, self.template_name, context)
            
            else:
                print("Equipment not registered !")
                context = {'form': Service2Form(), 'formset1': EquipmentFormSet(), 'formset2': StaffFormSet(), 'form1' : CategoryForm(), 'form2' : form2, 'form3' : StaffForm(), 'mnf' : mnf}
                return render(request, self.template_name, context)

        elif 'button3' in request.POST:
            form3 = self.form_class3(request.POST)

            if form3.is_valid():
                staff = form3.save()
                print("Staff registered !")
                context = {'form': Service2Form(), 'formset1': EquipmentFormSet(), 'formset2': StaffFormSet(), 'form1' : CategoryForm(), 'form2' : EquipmentForm(), 'form3' : StaffForm(), 'mnf' : mnf}
                return render(request, self.template_name, context)
            
            else:
                print("Staff not registered !")
                context = {'form': Service2Form(), 'formset1': EquipmentFormSet(), 'formset2': StaffFormSet(), 'form1' : CategoryForm(), 'form2' : EquipmentForm(), 'form3' : form3, 'mnf' : mnf}
                return render(request, self.template_name, context)