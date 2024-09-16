from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.contrib import messages
from .forms import AccountForm
from .models import AccountModel


# Create your views here.

def home(request):
    return render(request, 'base.html')


def accounts(request):
    context = {'account_form': AccountForm()}
    return render(request, 'account_add.html', context=context)


class AccountCreate(CreateView):
    model = AccountModel
    template_name = 'account_add.html'
    form_class = AccountForm
    context_object_name = 'account_form'
    success_url = reverse_lazy('account-add')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['account_form'] = context.pop('form')
        return context

    def form_valid(self, form):
        messages.success(self.request, "Account created successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error creating the account. Please try again.")
        return super().form_invalid(form)


class AccountList(ListView):
    model = AccountModel
    context_object_name = 'account_list'
    template_name = 'account_list.html'
    paginate_by = 10


class AccountUpdate(UpdateView):
    model = AccountModel
    form_class = AccountForm
    success_url = reverse_lazy('account-list')
    template_name = 'account_list.html'

    def form_invalid(self, form):
        messages.error(self.request, 'Unable to update account. Please try again.')
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, 'Account updated successfully.')
        return super().form_valid(form)


class AccountDelete(DeleteView):
    model = AccountModel
    success_url = reverse_lazy('account-list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(self.request, f'Account with ID {self.object.account_id} deleted successfully.')
            return response
        except Exception as e:
            messages.error(self.request, f'Error deleting account with ID {self.object.account_id}: {str(e)}')
            return self.render_to_response(self.get_context_data(object=self.object))
