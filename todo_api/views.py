from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from django.views import View
from todo_api.settings_local import SERVER_VERSION
from django.shortcuts import render

from . models import Note
from . import serializers, filters


class NoteListCreateAPIView(APIView):

    def get(self, request: Request):
        notes = Note.objects.all()
        serializer = serializers.NoteSerializer(
            instance=notes,
            many=True,
        )
        return Response(data=serializer.data)

    def post(self, request: Request):
        serializer = serializers.NoteSerializer(
            data=request.data
        )
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save(nt_author=request.user)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class NoteDetailAPIView(APIView):

    def get(self, request, pk):
        note = get_object_or_404(Note, pk=pk)
        serializer = serializers.NoteDetailSerializer(
            instance=note,
        )
        return Response(serializer.data)

    def put(self, request, pk):
        note = get_object_or_404(Note, pk=pk)
        serializer = serializers.NoteDetailSerializer(note, data=request.data)

        if not serializer.is_valid():
           return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if note.nt_author != request.user:
            return Response(f"Измения вносит только автор: {note.nt_author}",
                            status=status.HTTP_403_FORBIDDEN)

        serializer.save(nt_author=request.user)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request, pk):
        note = get_object_or_404(Note, pk=pk)
        serializer = serializers.NoteDetailSerializer(note, data=request.data, partial=True)

        if not serializer.is_valid():
           return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if note.nt_author != request.user:
            return Response(f"Измения вносит только автор: {note.nt_author}",
                            status=status.HTTP_403_FORBIDDEN)

        serializer.save(nt_author=request.user)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        note = get_object_or_404(Note, pk=pk)

        if note.nt_author != request.user:
            return Response(f"Измения вносит только автор: {note.nt_author}",
                            status=status.HTTP_403_FORBIDDEN)
        note.delete()

        return Response(f"Заметка №{pk} удалена.", status=status.HTTP_204_NO_CONTENT)


class PublicNoteListAPIView(ListAPIView):
    queryset = Note.objects.all()
    serializer_class = serializers.NoteSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(nt_author=1, nt_public=False).order_by("id")


    def filter_queryset(self, queryset):
        queryset = filters.note_filter_by_author_id(
            queryset,
            author_id=self.request.query_params.get("nt_author_id", None),
        )

        queryset = filters.note_filter_by_importance(queryset,
            importance_id=self.request.query_params.get("nt_importance", None),
            )

        return filters.note_filter_by_status(queryset,
            status_id=self.request.query_params.get("nt_status", None),
            )

class AboutAPIView(View):
    def get(self, request):
        context = {
            "server_version": SERVER_VERSION,
            "user_name": request.user.username

        }
        return render(
            request,
            "todo_api/about.html",
            context=context)