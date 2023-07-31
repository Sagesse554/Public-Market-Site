from django.shortcuts import render, redirect
from django.views import View
from reponses.forms import PaymentForm, OfferForm, ContractForm, IndicatorForm, Step2FormSet, VersionForm
from reponses.models import Etape2, Version

class PaymentView(View):
    template_name = 'payment.html'
    form_class = PaymentForm

    def get(self, request):
        form = self.form_class()
        cnt = request.GET.get('cnt')
        context = {'form' : form, 'cnt' : cnt}
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            cnt = request.GET.get('cnt')
            payment_data = form.cleaned_data
            payment_data['Cnt_numero'] = cnt
            Paiement.objects.create(**payment_data)
            print("Payment registered !")
            return redirect('home')

        else:
            print("Payment not registered !")
            cnt = request.GET.get('cnt')
            context = {'form' : form, 'cnt' : cnt}
            return render(request, self.template_name, context)


class OfferView(View):
    template_name = 'offer.html'
    form_class = OfferForm

    def get(self, request):
        form = self.form_class()
        apl = request.GET.get('apl')
        context = {'form' : form, 'apl' : apl}
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            apl = request.GET.get('apl')
            offer_data = form.cleaned_data
            offer_data['Apl_numero'] = apl
            offer_data['Ent_numero'] = request.user.Ent_numero
            offer_data['Ofr_conditions'] = Condition.objects.filter(Apl_numero=apl)
            Offre.objects.create(**offer_data)
            print("Offer registered !")
            return redirect('home')

        else:
            print("Offer not registered !")
            apl = request.GET.get('apl')
            context = {'form' : form, 'apl' : apl}
            return render(request, self.template_name, context)


class ContractView(View):
    template_name = 'contract.html'
    form_class1 = ContractForm
    form_class2 = VersionForm
    formset_class = Step2FormSet
    form_class3 = IndicatorForm
    
    def get(self, request):
        form1 = self.form_class1()
        form2 = self.form_class2()
        formset = self.formset_class()
        form3 = self.form_class3()
        ofr = request.GET.get('ofr')
        context = {'form1' : form1, 'form2' : form2, 'formset' : formset, 'form3' : form3, 'ofr' : ofr}
        return render(request, self.template_name, context)

    def post(self, request):
        ofr = request.GET.get('ofr')

        if 'button1' in request.POST:
            form1 = self.form_class1(request.POST)
            form2 = self.form_class2(request.POST, request.FILES, contract_form=form1)
            formset = self.formset_class(request.POST, contract_form=form1)

            if form1.is_valid() and form2.is_valid() and formset.is_valid():
                contract = form1.save()
                
                version_data = form2.cleaned_data
                version_data['Cnt_numero'] = contract
                Version.objects.create(**version_data)

                for form_step2 in formset:
                    step2_data = form_step2.cleaned_data
                    step2_data['Cnt_numero'] = contract
                    Etape2.objects.create(**step2_data)

                print("Contract registered !")
                return redirect('home')
            
            else:
                print("Contract not registered !")
                context = {'form1' : form1, 'form2' : form2, 'formset' : formset, 'form3' : IndicatorForm(), 'ofr' : ofr}
                return render(request, self.template_name, context)
            
        elif 'button2' in request.POST:
            form3 = self.form_class3(request.POST)

            if form3.is_valid():
                indicator = form3.save()
                print("Indicator registered !")    
                context = {'form1' : ContractForm(), 'form2' : VersionForm(), 'formset' : Step2FormSet(), 'form3' : IndicatorForm(), 'ofr' : ofr}
                return render(request, self.template_name, context)
            
            else:
                print("Indicator not registered !")
                context = {'form1' : ContractForm(), 'form2' : VersionForm(), 'formset' : Step2FormSet(), 'form3' : form3, 'ofr' : ofr}
                return render(request, self.template_name, context)
            