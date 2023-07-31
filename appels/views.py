from django.shortcuts import render, redirect
from django.views import View
from appels.forms import CallManifestForm, CallOfferForm, Service1Form, CategoryForm, CriteriaForm


class ManifestCallView(View):
    template_name = 'manifestcall.html'
    
    def get(self, request):
        return render(request, self.template_name)


class OfferCallView(View):
    template_name = 'offercall.html'
    
    def get(self, request):
        return render(request, self.template_name)


class CallManifestView(View):
    template_name = 'callmanifest.html'
    form_class = CallManifestForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form' : form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            manifestcall = form.save()
            print("Manifestation Call registered !")
            return redirect('home')

        else:
            print("Manifestation Call not registered !")
            return render(request, self.template_name, {'form': form})


class CallOfferView(View):
    template_name = 'calloffer.html'
    form_class = CallOfferForm
    form_class1 = Service1Form
    form_class2 = CategoryForm
    form_class3 = CriteriaForm

    def get(self, request):
        form = self.form_class()
        form1 = self.form_class1()
        form2 = self.form_class2()
        form3 = self.form_class3()
        context = {'form': form, 'form1': form1, 'form2' : form2, 'form3': form3}
        return render(request, self.template_name, context)

    def post(self, request):

        if 'button' in request.POST:
            form = self.form_class(request.POST, request.FILES)

            if form.is_valid():
                offercall = form.save()
                print("Offer Call registered !")
                return redirect('home')

            else:
                print("Offer Call not registered !")
                context = {'form': form, 'form1': Service1Form(), 'form2' : CategoryForm(), 'form3': CriteriaForm()}
                return render(request, self.template_name, context)

        elif 'button1' in request.POST:
            form1 = self.form_class1(request.POST)

            if form1.is_valid():
                service1 = form1.save()
                print("Service registered !")
                context = {'form': CallOfferForm(), 'form1': Service1Form(), 'form2' : CategoryForm(), 'form3': CriteriaForm()}
                return render(request, self.template_name, context)

            else:
                print("Service not registered !")
                context = {'form': CallOfferForm(), 'form1': form1, 'form2' : CategoryForm(), 'form3': CriteriaForm()}
                return render(request, self.template_name, context)

        elif 'button2' in request.POST:
            form2 = self.form_class2(request.POST)

            if form2.is_valid():
                category = form2.save()
                print("Category registered !")
                context = {'form': CallOfferForm(), 'form1': Service1Form(), 'form2' : CategoryForm(), 'form3': CriteriaForm()}
                return render(request, self.template_name, context)

            else:
                print("Category not registered !")
                context = {'form': CallOfferForm(), 'form1': Service1Form(), 'form2' : form2, 'form3': CriteriaForm()}
                return render(request, self.template_name, context)

        elif 'button3' in request.POST:
            form3 = self.form_class3(request.POST)

            if form3.is_valid():
                criteria = form3.save()
                print("Criteria registered !")
                context = {'form': CallOfferForm(), 'form1': Service1Form(), 'form2' : CategoryForm(), 'form3': CriteriaForm()}
                return render(request, self.template_name, context)

            else:
                print("Criteria not registered !")
                context = {'form': CallOfferForm(), 'form1': Service1Form(), 'form2' : CategoryForm(), 'form3': form3}
                return render(request, self.template_name, context)            