from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DetailView, FormView

from office_world.form import VoteAction
from office_world.models import VoteModel, VoteUser
from datetime import datetime
from django.db.models import F, Q


class VoteActiveView(TemplateView):
    template_name = 'office_world/home.html'

    def get(self, request, *args, **kwargs):
        valid_vote = get_valid_data()
        valid_data = Paginator(valid_vote, 50).get_page(request.GET.get('page'))
        return render(request, self.template_name, {'valid_data': valid_data})


class VoteActiveDetailView(DetailView):
    template_name = 'office_world/detail_view.html'
    model = VoteModel
    slug_field = 'name'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['voted_user'] = VoteUser.objects.filter(vote=self.object)
        result = int(self.object.date_end.strftime('%d')) - int(datetime.now().date().strftime('%d'))
        if result == 0:
            context['result'] = 'Сегодня последний день голосования'
        else:
            context['result'] = f'До конца голосования {result} д'

        return context


class VoteFormAction(FormView):
    slug_field = 'mac_addr'
    form_class = VoteAction
    success_url = '/'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            VoteUser.objects.filter(user=form.cleaned_data['user'], vote=form.cleaned_data['vote']).update(
                vote_count=F('vote_count') + 1)
            return self.form_valid(form)
        else:
            return redirect('/')


class VoteFinishedView(TemplateView):
    template_name = 'office_world/home_finished.html'

    def get(self, request, *args, **kwargs):
        valid = get_valid_data()
        invalid_vote = VoteModel.objects.filter(~Q(pk__in=valid)).all().order_by('id')
        invalid_data = Paginator(invalid_vote, 50).get_page(request.GET.get('page'))
        return render(request, self.template_name, {'valid_data': invalid_data})


class VoteFinishedDetailView(DetailView):
    template_name = 'office_world/detail_view_finished.html'
    model = VoteModel
    slug_field = 'name'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['voted_user'] = VoteUser.objects.filter(vote=self.object)
        return context


def get_valid_data() -> object:
    my_date = datetime.now().date()
    return VoteModel.objects.filter(date_start__lt=my_date,
                                    date_end__gte=my_date).exclude(~Q(max_vote=-1),
                                                                   persons__voteuser__vote_count__gte=F(
                                                                       'max_vote')).all().order_by('id')
