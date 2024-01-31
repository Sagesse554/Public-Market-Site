from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Max
from django.urls import reverse
from django.views import View
from random import randint
from reponses.forms import PaymentForm, OfferForm, ContractForm, IndicatorForm, VersionForm
from reponses.models import Paiement, Etape2, Version, Offre, Contrat, Evaluation1, Evaluation2
from entreprises.models import Entreprise, Registre
from appels.models import Appel_d_Offre, Condition


class OffreView(LoginRequiredMixin, View):
    template_name = 'offre.html'
    
    def get(self, request):
        context = {}
        ofr = request.GET.get('ofr')
        if ofr is not None:
            ofr = Offre.objects.filter(Ofr_numero=ofr)
            ofr.evaluations = Evaluation1.objects.filter(Ofr_numero=ofr)
            context['ofr'] = ofr
            return render(request, self.template_name, context) 
        else:
            return redirect("offres")


class ContratView(LoginRequiredMixin, View):
    template_name = 'contrat.html'
    
    def get(self, request):
        context = {}
        cnt = request.GET.get('cnt')
        if cnt is not None:
            cnt = Contrat.objects.filter(Cnt_numero=cnt)
            last_version_moment = Version.objects.filter(Q(Cnt_numero=cnt) & Q(Vrs_statut='VALIDE')).aggregate(last_version_moment=Max('Vrs_moment'))['last_version_moment']
            vrs = Version.objects.get(Q(Cnt_numero=cnt) & Q(Vrs_moment=last_version_moment))
            cnt.vrs = vrs
            cnt.etapes = Etape2.objects.filter(Cnt_numero=cnt)
            cnt.paiements = Paiement.objects.filter(Cnt_numero=cnt)
            cnt.evaluations = Evaluation2.objects.filter(Cnt_numero=cnt)
            context['cnt'] = cnt
            return render(request, self.template_name, context) 
        else:
            return redirect('contrats')


class OffresView(LoginRequiredMixin, View):
    template_name = 'offres.html'
    
    def get(self, request):
        context = {}
        if request.user.Ent_numero.Ent_numero.Rgs_numero != '1613978901':
            ofr = Offre.objects.filter(Ent_numero=request.user.Ent_numero)
            ofrn = ofr.count()
            for of in ofr:
                of.cnt = Contrat.objects.filter(Ofr_numero=of)
            if ofrn != 0:
                context['ofr'] = ofr
                context['ofrn'] = ofrn
            else:
                context['ofrn'] = ofrn
            return render(request, self.template_name, context)   
        else:
            apl = request.GET.get('apl')
            if apl is not None:
                context['apl'] = apl
                ofr = Offre.objects.filter(Apl_numero=apl)
                ofrn = ofr.count()
                if ofrn != 0:
                    context['apl'] = apl
                    context['ofr'] = ofr
                    context['ofrn'] = ofrn
                else:
                    context['ofrn'] = ofrn
                return render(request, self.template_name, context)
            else:
                return redirect('offercall')
        return render(request, self.template_name, context)


class ContratsView(LoginRequiredMixin, View):
    template_name = 'contrats.html'
    
    def get(self, request):
        context = {}
        if request.user.Ent_numero.Ent_numero.Rgs_numero != '1613978901':
            ofr = Offre.objects.filter(Ent_numero=request.user.Ent_numero)
            cnt = Contrat.objects.filter(Ofr_numero__in=ofr)
            cntn = cnt.count()
            for cn in cnt:
                last_version_moment = Version.objects.filter(Q(Cnt_numero=cn) & Q(Vrs_statut='VALIDE')).aggregate(last_version_moment=Max('Vrs_moment'))['last_version_moment']
                vrs = Version.objects.get(Q(Cnt_numero=cn) & Q(Vrs_moment=last_version_moment))
                cn.vrs = vrs
                cn.etape_count = Etape2.objects.filter(Cnt_numero=cn).count()
            if cntn != 0:
                context['cnt'] = cnt
                context['cntn'] = cntn
            else:
                context['cntn'] = cntn
        else:
            cntc = Contrat.objects.filter(Cnt_statut='EN_COURS')
            for cnt in cntc:
                last_version_moment = Version.objects.filter(Q(Cnt_numero=cnt)).aggregate(last_version_moment=Max('Vrs_moment'))['last_version_moment']
                vrs = Version.objects.get(Q(Cnt_numero=cnt) & Q(Vrs_moment=last_version_moment))
                cnt.vrs = vrs
                cnt.etape_count = Etape2.objects.filter(Cnt_numero=cnt).count()
            cntcn = cntc.count()
            if cntcn != 0:
                context['cntc'] = cntc
                context['cntcn'] = cntcn
            else:
                context['cntcn'] = cntcn
        return render(request, self.template_name, context)


class PaymentView(LoginRequiredMixin, View):
    template_name = 'payment.html'
    form_class = PaymentForm

    def get(self, request):
        if request.user.Ent_numero.Ent_numero.Rgs_numero == '1613978901':
            form = self.form_class()
            cnt = request.GET.get('cnt')
            if cnt is not None:
                context = {'form' : form, 'cnt' : cnt}
                return render(request, self.template_name, context)
            else:
                return redirect('contrats')
        else:
            return redirect(f"{reverse('signin')}?next=/payment/")

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            #cnt = request.POST.get('cnt')
            cnt = Contrat.objects.first()
            payment_data = form.cleaned_data
            payment_data['Cnt_numero'] = cnt
            Paiement.objects.create(**payment_data)
            print("Payment registered !")
            return redirect("home")
        else:
            print("Payment not registered !")
            cnt = request.POST.get('cnt')
            context = {'form' : form, 'cnt' : cnt}
            return render(request, self.template_name, context)


class OfferView(LoginRequiredMixin, View):
    template_name = 'offer.html'
    form_class = OfferForm

    def get(self, request):
        if request.user.Ent_numero.Ent_numero.Rgs_numero != '1613978901':
            form = self.form_class()
            apl = request.GET.get('apl')
            context = {'form' : form, 'apl' : apl}
            return render(request, self.template_name, context)
        else:
            return redirect(f"{reverse('signin')}?next=/offer/")

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            apl = request.POST.get('apl')
            ent = request.user.Ent_numero
            offer_data = form.cleaned_data
            offer_data['Apl_numero'] = apl
            offer_data['Ent_numero'] = ent
            Offre.objects.create(**offer_data)
            offer = Offre.objects.get(Ofr_numero=offer_data['Ofr_numero'])
            conditions = Condition.objects.filter(Apl_numero=apl)
            for condition in conditions:
                offer.Ofr_conditions.set(condition)
                evl1 = Evaluation1.objects.get(Q(Cnd_id=condition) & Q(Ofr_numero=offer))
                evl1.Evl1_note = randint(60,100)
            ent.Ent_evaluation = randint(60,100)
            print("Offer registered !")
            return redirect("home")

        else:
            print("Offer not registered !")
            apl = request.GET.get('apl')
            context = {'form' : form, 'apl' : apl}
            return render(request, self.template_name, context)


class ContractView(LoginRequiredMixin, View):
    template_name = 'contract.html'
    form_class1 = ContractForm
    form_class2 = VersionForm
    #formset_class = Step2FormSet
    form_class3 = IndicatorForm
    
    def get(self, request):
        if request.user.Ent_numero.Ent_numero.Rgs_numero == '1613978901':
            form1 = self.form_class1()
            form2 = self.form_class2()
            #formset = self.formset_class()
            form3 = self.form_class3()
            ofr = request.GET.get('ofr')
            context = {'form1' : form1, 'form2' : form2, 'form3' : form3, 'ofr' : ofr}
            #context = {'form1' : form1, 'form2' : form2, 'formset' : formset, 'form3' : form3, 'ofr' : ofr}
            return render(request, self.template_name, context)
        else:
            return redirect(f"{reverse('signin')}?next=/contract/")

    def post(self, request):
        ofr = request.GET.get('ofr')

        if 'button1' in request.POST:
            form1 = self.form_class1(request.POST)
            form2 = self.form_class2(request.POST, request.FILES)
            #formset = self.formset_class(request.POST)

            if form1.is_valid() and form2.is_valid():
            #if form1.is_valid() and form2.is_valid() and formset.is_valid():
                ofr = request.POST.get('ofr')
                contract_data = form1.cleaned_data
                contract_data['Ofr_numero'] = ofr
                indicateurs = contract_data.pop('Cnt_indicateurs')
                contract = Contrat(**contract_data)
                contract.save()
                for indicateur in indicateurs:
                    contract.Cnt_indicateurs.add(indicateur)
                    evl2 = Evaluation2.objects.get(Q(Ind_id=indicateur) & Q(Cnt_numero=contract))
                    evl2.Evl2_note = randint(60,100)                
                version_data = form2.cleaned_data
                version_data['Cnt_numero'] = contract
                Version.objects.create(**version_data)

                """for form_step2 in formset:
                    step2_data = form_step2.cleaned_data
                    step2_data['Cnt_numero'] = contract
                    Etape2.objects.create(**step2_data)"""

                print("Contract registered !")
                return redirect("home")
            
            else:
                print("Contract not registered !")
                context = {'form1' : form1, 'form2' : form2, 'form3' : IndicatorForm(), 'ofr' : ofr}
                #context = {'form1' : form1, 'form2' : form2, 'formset' : formset, 'form3' : IndicatorForm(), 'ofr' : ofr}
                return render(request, self.template_name, context)
            
        elif 'button2' in request.POST:
            form3 = self.form_class3(request.POST)

            if form3.is_valid():
                indicator = form3.save()
                print("Indicator registered !")    
                context = {'form1' : ContractForm(), 'form2' : VersionForm(), 'form3' : IndicatorForm(), 'ofr' : ofr}
                #context = {'form1' : ContractForm(), 'form2' : VersionForm(), 'formset' : Step2FormSet(), 'form3' : IndicatorForm(), 'ofr' : ofr}
                return render(request, self.template_name, context)
            
            else:
                print("Indicator not registered !")
                context = {'form1' : ContractForm(), 'form2' : VersionForm(), 'form3' : form3, 'ofr' : ofr}
                #context = {'form1' : ContractForm(), 'form2' : VersionForm(), 'formset' : Step2FormSet(), 'form3' : form3, 'ofr' : ofr}
                return render(request, self.template_name, context)