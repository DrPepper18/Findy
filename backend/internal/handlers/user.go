package handlers

import (
	"context"
	"log"
	"net/http"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/jwtauth/v5"
	"github.com/go-chi/render"
	"github.com/google/uuid"

	"find_a_walk/internal/domain"
)

type UserService interface {
	Login(ctx context.Context, user *domain.UserAuth) (*domain.Token, error)
	GetUserByID(ctx context.Context, id uuid.UUID) (*domain.User, error)
	CreateUser(ctx context.Context, user *domain.UserIn) (*domain.User, error)
	GetJWTConfig() *jwtauth.JWTAuth
}

// Обработчики HTTP запросов
type UserHandler struct {
	service UserService
}

func NewUserHandler(service UserService) *UserHandler {
	return &UserHandler{service: service}
}

func (h *UserHandler) GetUserByID(w http.ResponseWriter, r *http.Request) {
	_, claims, err := jwtauth.FromContext(r.Context())
	if err != nil {
		render.Render(w, r, domain.ErrInvalidRequest(err, http.StatusBadRequest))
		return
	}
	log.Println(claims)

	id := chi.URLParam(r, "id")

	userID, err := uuid.Parse(id)
	if err != nil {
		render.Render(w, r, domain.ErrInvalidRequest(err, http.StatusBadRequest))
		return
	}

	user, err := h.service.GetUserByID(r.Context(), userID)
	if err != nil {
		render.Render(w, r, domain.ErrInvalidRequest(err, http.StatusNotFound))
		return
	}

	render.Render(w, r, user)
}

func (h *UserHandler) CreateUser(w http.ResponseWriter, r *http.Request) {
	userSchema := &domain.UserIn{}
	err := render.Bind(r, userSchema)
	if err != nil {
		render.Render(w, r, domain.ErrInvalidRequest(err, http.StatusBadRequest))
		return
	}

	user, err := h.service.CreateUser(r.Context(), userSchema)
	if err != nil {
		render.Render(w, r, domain.ErrInvalidRequest(err, http.StatusInternalServerError))
		return
	}

	render.Status(r, http.StatusCreated)
	render.Render(w, r, user)
}
