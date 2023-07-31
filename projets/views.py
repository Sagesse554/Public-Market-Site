from django.shortcuts import render, redirect
from django.views import View
from projets.models import Etape1
from projets.forms import ProjectForm, Step1FormSet


class ProjectView(View):
    template_name = 'projet.html'
    form_class = ProjectForm
    formset_class = Step1FormSet

    def get(self, request):
        form = self.form_class()
        formset = self.formset_class()
        return render(request, self.template_name, {'form': form, 'formset': formset})

    def post(self, request):
        form = self.form_class(request, data=request.POST)
        formset = self.formset_class(request.POST, project_form=form)

        if form.is_valid() and formset.is_valid():
            project_data = form.cleaned_data
            budgetsum = 0
            
            for form_step1 in formset:
                step1_data = form_step1.cleaned_data
                budgetsum += step1_data['Etp1_budget']
            
            if budgetsum <= project_data['Pjt_budget']:
                project = form.save()
            
                for form_step1 in formset:
                    step1_data = form_step1.cleaned_data
                    step1_data['Pjt_numero'] = project
                    Etape1.objects.create(**step1_data)
            
                print("Project registration successful!")
                return redirect('home')
            
            else:
                print('Project registration failed!')
                form.add_error('Pjt_budget', 'La somme des budgets d\'étape ne peut dépasser le budget de projet !')
                return render(request, self.template_name, {'form': form, 'formset': formset})
        
        else:
            print('Project registration failed!')
            return render(request, self.template_name, {'form': form, 'formset': formset})