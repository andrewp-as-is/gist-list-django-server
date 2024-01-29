from django.apps import apps
from django.conf import settings
from django.db.models import Count, Q
from django.shortcuts import redirect

from base.apps.github.models import Trash
from views.base import ListView
from views.details import Details
from ..mixins import UserMixin
from .utils import (
    get_object,
    get_gist_model,
    get_language,
    get_language_item_list,
    get_language_stat,
    get_stat_data,
    get_tag_item_list,
    get_tag_stat,
    get_tag,
)
from . import details


class View(UserMixin, ListView):
    context_object_name = "gist_list"
    template_name = "user/gists/gist_list.html"

    def get_model(self):
        return get_gist_model(self.github_user_stat)

    def get(self, request, *args, **kwargs):
        login = self.kwargs.get("login")
        if request.path == "/%s/" % login:
            return redirect("/%s" % login)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_data = context.get('context_data',{})
        if self.github_user:
            user_id = self.github_user.id
            secret = (
                self.request.user.is_authenticated
                and self.request.user.login == self.github_user.login
            )
           # if is_owner:
           #     context["blankslate"] = (
           #         not self.github_user.public_gists_count
           #         and not self.github_user.private_gists_count
           ##     )
           # else:
            #    context["blankslate"] = not self.github_user.public_gists_count
            # count = self.get_queryset_base().count()
            # todo: remake queryset_count
            # todo: stat tags/etc
            # context["queryset_count"] = count
            model = self.get_model()
            if self.github_user_stat:
                language_stat = get_stat_data(self.github_user_stat.public_language_stat)
                tag_stat = get_stat_data(self.github_user_stat.public_tag_stat)
                if secret:
                    language_stat = get_stat_data(self.github_user_stat.secret_language_stat)
                    tag_stat = get_stat_data(self.github_user_stat.secret_tag_stat)
                context_data["languages_count"] = len(language_stat.keys())
                # context["tags_count"] = len(tag_stat.keys())
                context_data['details'] = dict(
                    language = Details(
                        self.request,
                        menu_item_list=get_language_item_list(language_stat),
                    ),
                        tag = Details(
                        self.request,
                        menu_item_list=get_tag_item_list(tag_stat),
                    ),
                    sort = details.Sort(self.request),
                    type = details.Type(
                        self.request, github_user=self.github_user
                    )
                )
        context['context_data'] = context_data
        return context

    def get_queryset_base(self, **kwargs):
        model = self.get_model()
        if (
            not hasattr(self, "github_user")
            or not self.github_user
        ):
            return model.objects.none()
        qs = model.objects.filter(owner_id=self.github_user.id)
        if (
            not self.request.user.is_authenticated
            or self.github_user.login != self.request.user.login
        ):
            qs = qs.filter(public=True)
        return qs

    def get_queryset(self, **kwargs):
        model = self.get_model()
        if (
            not hasattr(self, "github_user")
            or not self.github_user
        ):
            return model.objects.none()
        prefix = "gist__" if self.request.path.split("/")[-1] == "starred" else ""
        qs = self.get_queryset_base()
        qs = qs.exclude(
            id__in=Trash.objects.values_list("gist_id", flat=True)
        )  # live gists only
        language_value = self.request.GET.get("language", "").strip().lower()
        if language_value:
            language = get_language(language_value)
            if language:
                # qs = qs.filter(language_m2m=language.id)
                qs = qs.filter(
                    id__in=self.gist_language_model.objects.filter(
                        gist_id__in=self.get_queryset_base().values_list(
                            "id", flat=True
                        ),
                        language_id=language.id,
                    ).values_list("gist_id", flat=True)
                )
            if language_value == "none":
                # qs = qs.filter(language_m2m=None)
                qs = qs.exclude(
                    id__in=self.gist_language_model.objects.filter(
                        gist_id__in=self.get_queryset_base().values_list(
                            "id", flat=True
                        )
                    ).values_list("gist_id", flat=True)
                )
        tag_slug = self.request.GET.get("tag", "").strip().lower()
        if tag_slug:
            tag = get_tag(tag_slug)
            if tag:
                # qs = qs.filter(tag_m2m=tag.id)
                qs = qs.filter(
                    id__in=self.gist_tag_model.objects.filter(
                        gist_id__in=self.get_queryset_base().values_list(
                            "id", flat=True
                        ),
                        tag_id=tag.id,
                    ).values_list("gist_id", flat=True)
                )
            if tag_slug == "none":
                # qs = qs.filter(tag_m2m=None)
                qs = qs.exclude(
                    id__in=self.gist_tag_model.objects.filter(
                        gist_id__in=self.get_queryset_base().values_list(
                            "id", flat=True
                        )
                    ).values_list("gist_id", flat=True)
                )
        q = self.request.GET.get("q", "").strip()
        if q:
            # todo: check q = gist ID (0-9A-F)
            # todo: check q = language. index?
            # language: xml = must search gists with "xml property list" language
            # 1) find language
            # 2) find gists with language__in=
            # todo: filename. make index
            # todo: description (if tsv not works)
            # todo: tsv
            # todo: tags
            # todo: preload filenames and compare in memory?
            qs = qs.filter(
                Q(**{"id": q})
                | Q(**{"description__icontains": q})
                # Q(**{'filename__icontains':q})
                # Q(**{'languages__icontains':q})
            )
        order_by_list = self.get_queryset_order_by_list()
        return qs.order_by(*order_by_list)

    def get_queryset_order_by_list(self, **kwargs):
        model = self.get_model()
        sort = self.request.GET.get("sort", "")
        sort_prefix = "-" if sort and sort[0] == "-" else ""
        sort_column = self.request.GET.get("sort", "").replace("-", "")
        order_by = ["created_order"]
        if hasattr(model, "%s_order" % sort_column):
            order_by = [sort_prefix + "%s_order" % sort_column]
        return order_by
