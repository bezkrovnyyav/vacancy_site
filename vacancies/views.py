from django.db.models import Count
from django.http import HttpResponseNotFound, HttpResponseServerError, Http404


from django.views.generic import TemplateView

from vacancies.models import Specialty, Vacancy, Company


class MainView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context['specialties'] = Specialty.objects.annotate(vacancies_count=Count('vacancies'))
        context['companies'] = Company.objects.annotate(vacancies_count=Count('vacancies'))
        return context


class SpecialVacancyView(TemplateView):
    template_name = "vacancies.html"

    def get_context_data(self, **kwargs):
        context = super(SpecialVacancyView, self).get_context_data(**kwargs)
        specialty_code = kwargs['specialty_code']
        try:
            specialty = Specialty.objects.get(code=specialty_code)
            vacancies = Vacancy.objects.filter(specialty__code=specialty_code)
            context['specialty'] = specialty
            context['vacancies'] = vacancies
        except Specialty.DoesNotExist:
            raise Http404(f"Код '{specialty_code}' не найден!")
        return context


class AllVacancyView(TemplateView):
    template_name = "vacancies.html"

    def get_context_data(self, **kwargs):
        context = super(AllVacancyView, self).get_context_data(**kwargs)
        context['vacancies'] = Vacancy.objects.all()
        return context


class CompanyView(TemplateView):
    template_name = "company.html"

    def get_context_data(self, **kwargs):
        context = super(CompanyView, self).get_context_data(**kwargs)
        company_id = int(self.kwargs['company_id'])
        try:
            context['company'] = Company.objects.get(id=company_id)
            context['vacancies'] = Vacancy.objects.filter(company__id=company_id)
        except Company.DoesNotExist:
            raise Http404(f"Компания id={company_id} не найдена!")
        return context


class VacancyView(TemplateView):
    template_name = "vacancy.html"

    def get_context_data(self, **kwargs):
        context = super(VacancyView, self).get_context_data(**kwargs)
        vacancy_id = int(self.kwargs['vacancy_id'])
        try:
            context['vacancy'] = Vacancy.objects.get(id=vacancy_id)
        except Vacancy.DoesNotExist:
            raise Http404(f"Код id={vacancy_id} не найден!")
        return context


def custom_handler404(request, exception):
    # Call when Http404 raised
    return HttpResponseNotFound('Ресурс не найден!')


def custom_handler500(request):
    # Call when raised some python exception
    return HttpResponseServerError('Ошибка сервера!')
