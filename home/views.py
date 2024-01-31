from datetime import timedelta
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.utils import timezone
from django.db.models import Q, Max
from entreprises.models import Entreprise, Manifestation
from appels.models import Appel_d_Offre, Appel_a_Manifestation
from reponses.models import Contrat, Offre, Version, Etape2
from projets.models import Projet_d_Approvisionnement


def IndexView(request):

    print('On the dashboard!')
    apls = Appel_d_Offre.objects.count()
    entn = Entreprise.objects.count()
    cnts = Contrat.objects.count()
    amic = Appel_a_Manifestation.objects.filter(Ami_statut='EN_COURS')
    amicn = amic.count()
    aplc = Appel_d_Offre.objects.filter(Apl_statut='EN_COURS')
    aplcn = aplc.count()
    for apl in aplc:
        apl.offre_count = Offre.objects.filter(Apl_numero=apl).count()
    for ami in amic:
        ami.entreprise_count = Manifestation.objects.filter(Ami_numero=ami).count()
    context = {'apls' : apls, 'entn' : entn, 'cnts' : cnts, 'amic' : amic, 'aplc' : aplc, 'amicn' : amicn, 'aplcn' : aplcn}
    if request.user.is_authenticated:
        if request.user.Ent_numero.Ent_numero.Rgs_numero != '1613978901':
            ofr = Offre.objects.filter(Ent_numero=request.user.Ent_numero)
            ofrn = ofr.count()
            cnt = Contrat.objects.filter(Ofr_numero__in=ofr)
            cntn = cnt.count()
            for cn in cnt:
                last_version_moment = Version.objects.filter(Q(Cnt_numero=cn) & Q(Vrs_statut='VALIDE')).aggregate(last_version_moment=Max('Vrs_moment'))['last_version_moment']
                vrs = Version.objects.get(Q(Cnt_numero=cn) & Q(Vrs_moment=last_version_moment))
                cn.vrs = vrs
                cn.etape_count = Etape2.objects.filter(Cnt_numero=cn).count()
            if ofrn != 0:
                if cntn != 0:
                    context['ofr'] = ofr
                    context['cnt'] = cnt
                    context['ofrn'] = ofrn
                    context['cntn'] = cntn
                else:
                    context['ofr'] = ofr
                    context['ofrn'] = ofrn
                    context['cntn'] = cntn
            else:
                context['ofrn'] = ofrn     
        else:
            pjt = Projet_d_Approvisionnement.objects.filter(Pjt_statut='EN_COURS')
            for pj in pjt:
                pj.appel_count = Appel_d_Offre.objects.filter(Pjt_numero=pj).count()
            pjtn = pjt.count()
            cntc = Contrat.objects.filter(Cnt_statut='EN_COURS')
            for cnt in cntc:
                last_version_moment = Version.objects.filter(Q(Cnt_numero=cnt)).aggregate(last_version_moment=Max('Vrs_moment'))['last_version_moment']
                vrs = Version.objects.get(Q(Cnt_numero=cnt) & Q(Vrs_moment=last_version_moment))
                cnt.vrs = vrs
                cnt.etape_count = Etape2.objects.filter(Cnt_numero=cnt).count()
            cntcn = cntc.count()
            mnfs, entv, mnfv = Manifestation.objects.all(), [], []
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
            if pjtn != 0:
                context['pjt'] = pjt
                context['pjtn'] = pjtn
            else:
                context['pjtn'] = pjtn
            if cntcn != 0:
                context['cntc'] = cntc
                context['cntcn'] = cntcn
            else:
                context['cntcn'] = cntcn
            if entsn != 0:
                context['ents'] = ents
                context['entsn'] = entsn
            else:
                context['entsn'] = entsn
    return render(request, 'index.html', context)


def LogoutView(request):
    
    logout(request)
    print('Successfully disconnected!')
    return redirect('home')