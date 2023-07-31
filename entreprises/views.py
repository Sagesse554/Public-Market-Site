from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from entreprises.models import Manifestation, Reference, Allocation1, Allocation2
from entreprises.forms import EnterpriseForm, ManifestForm, ReferenceForm, Service3FormSet, Service2Form, EquipmentFormSet, StaffFormSet, EquipmentForm, StaffForm
from appels.forms import CategoryForm


class ManifestView(LoginRequiredMixin, View):
    template_name = 'manifest.html'
    form_class1 = EnterpriseForm
    form_class2 = ManifestForm

    def get(self, request):
        form1 = self.form_class1()
        form2 = self.form_class2()
        ami = request.GET.get('ami')
        next_url = request.GET.get('next', '')
        context = {'form1': form1, 'form2' : form2, 'ami' : ami, 'next': next_url}
        return render(request, self.template_name, context)

    def post(self, request):
        form1 = self.form_class1(request.POST)
        form2 = self.form_class2(request.POST, request.FILES)

        if form1.is_valid() and form2.is_valid():
            enterprise = form1.save()
            
            ami = request.GET.get('ami')
            manifest_data = form2.cleaned_data
            manifest_data['Ami_numero'] = ami
            manifest_data['Ent_numero'] = enterprise
            Manifestation.objects.create(**manifest_data)
            
            print("Enterprise registered successfully!")
            next_url = request.POST.get('next', '')
            
            if next_url:
                return redirect(next_url)
            else:
                return redirect('home')

        else:
            print("Enterprise registration failed!")
            next_url = request.POST.get('next', '')
            ami = request.GET.get('ami')
            context = {'form1': form1, 'form2' : form2, 'next': next_url, 'ami' : ami}
            return render(request, self.template_name, context)


class ReferenceView(View):
    template_name = 'reference.html'
    form_class1 = ReferenceForm
    formset_class = Service3FormSet
    form_class2 = CategoryForm

    def get(self, request):
        form1 = self.form_class1()
        formset = self.formset_class()
        form2 = self.form_class2()
        ent = request.GET.get('ent')
        context = {'form1': form1, 'formset': formset, 'form2' : form2, 'ent' : ent}
        return render(request, self.template_name, context)

    def post(self, request):        
        ent = request.GET.get('ent')

        if 'button1' in request.POST:
            form1 = self.form_class1(request.POST, request.FILES)
            formset = self.formset_class(request.POST, reference_form=form1)

            if form1.is_valid() and formset.is_valid():    
                reference_data = form1.cleaned_data
                reference_data['Ent_numero'] = ent
                Reference.objects.create(**reference_data)

                for form_service3 in formset:
                    service3_data = form_service3.cleaned_data
                    service3_data['Rfc_id'] = reference
                    Prestation3.objects.create(**service3_data)

                print("Reference registration successful !")
                return redirect('home')
            
            else:
                print("Reference registration failed !")
                context = {'form1': form1, 'formset': formset, 'form2' : CategoryForm(), 'ent' : ent}
                return render(request, self.template_name, context)
            
        elif 'button2' in request.POST:
            form2 = self.form_class2(request.POST)

            if form2.is_valid():
                category = form2.save()
                print("Category registered !")    
                context = {'form1': ReferenceForm(), 'formset': Service3FormSet(), 'form2' : CategoryForm(), 'ent' : ent}
                return render(request, self.template_name, context)
            
            else:
                print("Category registered !")
                context = {'form1': ReferenceForm(), 'formset': Service3FormSet(), 'form2' : form2, 'ent' : ent}
                return render(request, self.template_name, context)
            


class Service2View(View):
    template_name = 'service.html'
    form_class =   Service2Form
    formset_class1 = EquipmentFormSet
    formset_class2 = StaffFormSet
    form_class1 = CategoryForm
    form_class2 = EquipmentForm
    form_class3 = StaffForm

    def get(self, request):
        form = self.form_class()
        formset1 = self.formset_class1()
        formset2 = self.formset_class2()
        form1 = self.form_class1()
        form2 = self.form_class2()
        form3 = self.form_class3()
        mnf = request.GET.get('mnf')
        context = {'form': form, 'formset1': formset1, 'formset2': formset2, 'form1' : form1, 'form2' : form2, 'form3' : form3, 'mnf' : mnf}
        return render(request, self.template_name, context)

    def post(self, request):        
        mnf = request.GET.get('mnf')

        if 'button' in request.POST:
            form = self.form_class(request.POST)
            formset1 = self.formset_class1(request.POST, service2_form=form)
            formset2 = self.formset_class2(request.POST, service2_form=form)

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