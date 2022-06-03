from django.db.models.query import QuerySet
from typing import Optional


def note_filter_by_author_id(queryset: QuerySet, author_id: Optional[int]):
    """
    Фильтр по id
    """
    if author_id:
        return queryset.filter(nt_author_id=author_id)
    else:
        return queryset


def note_filter_by_importance(queryset: QuerySet, importance_id: Optional[bool]):
    """
    Фильтр по важности
    """
    if importance_id:
        return queryset.filter(nt_importance=importance_id)
    else:
        return queryset


def note_filter_by_status(queryset: QuerySet, status_id: Optional[int]):
    """
    Фильтр по статусу
    """
    if status_id:
        return queryset.filter(nt_status=status_id)
    else:
        return queryset