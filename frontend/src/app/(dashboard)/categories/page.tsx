"use client";

import { useState, useEffect } from "react";
import { useAuth } from "@/lib/auth-context";
import { apiClient } from "@/lib/api-client";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Skeleton } from "@/components/ui/skeleton";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { toast } from "sonner";

interface Category {
  id: string;
  name: string;
  color?: string;
  icon?: string;
  budget_limit?: number;
}

export default function CategoriesPage() {
  const { token } = useAuth();
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editDialogOpen, setEditDialogOpen] = useState(false);
  const [editingCategory, setEditingCategory] = useState<Category | null>(null);

  const [formData, setFormData] = useState({
    name: "",
    color: "#3b82f6",
    budget_limit: "",
  });

  useEffect(() => {
    loadCategories();
  }, []);

  const loadCategories = async () => {
    if (!token) return;

    try {
      setLoading(true);
      const data = await apiClient.getCategories(token);
      setCategories(data);
    } catch (error) {
      console.error("Erro ao carregar categorias:", error);
      toast.error("Erro ao carregar categorias");
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!token) return;

    try {
      const payload: any = {
        name: formData.name,
        color: formData.color,
      };

      if (formData.budget_limit) {
        payload.budget_limit = parseFloat(formData.budget_limit);
      }

      await apiClient.createCategory(token, payload);

      toast.success("Categoria criada com sucesso!");
      setDialogOpen(false);
      setFormData({
        name: "",
        color: "#3b82f6",
        budget_limit: "",
      });
      loadCategories();
    } catch (error: any) {
      toast.error("Erro ao criar categoria: " + error.message);
    }
  };

  const handleEdit = (category: Category) => {
    setEditingCategory(category);
    setFormData({
      name: category.name,
      color: category.color || "#3b82f6",
      budget_limit: category.budget_limit?.toString() || "",
    });
    setEditDialogOpen(true);
  };

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!token || !editingCategory) return;

    try {
      const payload: any = {
        name: formData.name,
        color: formData.color,
      };

      if (formData.budget_limit) {
        payload.budget_limit = parseFloat(formData.budget_limit);
      } else {
        payload.budget_limit = null;
      }

      await apiClient.updateCategory(token, editingCategory.id, payload);

      toast.success("Categoria atualizada!");
      setEditDialogOpen(false);
      setEditingCategory(null);
      loadCategories();
    } catch (error: any) {
      toast.error("Erro ao atualizar: " + error.message);
    }
  };

  const handleDelete = async (id: string, name: string) => {
    if (!token) return;
    if (!confirm(`Deseja realmente deletar a categoria "${name}"?`)) return;

    try {
      await apiClient.deleteCategory(token, id);
      toast.success("Categoria deletada!");
      loadCategories();
    } catch (error: any) {
      toast.error("Erro ao deletar: " + error.message);
    }
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat("pt-BR", {
      style: "currency",
      currency: "BRL",
    }).format(value);
  };

  const CategoryForm = ({ onSubmit, isEdit = false }: any) => (
    <form onSubmit={onSubmit} className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="name">Nome</Label>
        <Input
          id="name"
          type="text"
          value={formData.name}
          onChange={(e) =>
            setFormData({ ...formData, name: e.target.value })
          }
          placeholder="Ex: Alimentação"
          required
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="color">Cor</Label>
        <div className="flex gap-2">
          <Input
            id="color"
            type="color"
            value={formData.color}
            onChange={(e) =>
              setFormData({ ...formData, color: e.target.value })
            }
            className="w-20 h-10"
          />
          <Input
            type="text"
            value={formData.color}
            onChange={(e) =>
              setFormData({ ...formData, color: e.target.value })
            }
            placeholder="#3b82f6"
          />
        </div>
      </div>

      <div className="space-y-2">
        <Label htmlFor="budget_limit">Limite Mensal (opcional)</Label>
        <Input
          id="budget_limit"
          type="number"
          step="0.01"
          value={formData.budget_limit}
          onChange={(e) =>
            setFormData({ ...formData, budget_limit: e.target.value })
          }
          placeholder="0.00"
        />
        <p className="text-xs text-gray-500">
          Defina um limite de gastos mensal para esta categoria
        </p>
      </div>

      <div className="flex justify-end gap-2">
        <Button
          type="button"
          variant="outline"
          onClick={() => {
            if (isEdit) {
              setEditDialogOpen(false);
            } else {
              setDialogOpen(false);
            }
          }}
        >
          Cancelar
        </Button>
        <Button type="submit">{isEdit ? "Atualizar" : "Salvar"}</Button>
      </div>
    </form>
  );

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">Categorias</h2>
          <p className="text-gray-600">Organize suas transações por categoria</p>
        </div>
        <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
          <DialogTrigger asChild>
            <Button>Nova Categoria</Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Adicionar Categoria</DialogTitle>
              <DialogDescription>
                Crie uma nova categoria para organizar suas transações
              </DialogDescription>
            </DialogHeader>
            <CategoryForm onSubmit={handleSubmit} />
          </DialogContent>
        </Dialog>
      </div>

      {/* Dialog de Edição */}
      <Dialog open={editDialogOpen} onOpenChange={setEditDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Editar Categoria</DialogTitle>
            <DialogDescription>
              Altere os dados da categoria
            </DialogDescription>
          </DialogHeader>
          <CategoryForm onSubmit={handleUpdate} isEdit={true} />
        </DialogContent>
      </Dialog>

      {loading ? (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <Card key={i}>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2 flex-1">
                    <Skeleton className="w-4 h-4 rounded-full" />
                    <Skeleton className="h-5 w-32" />
                  </div>
                  <div className="flex gap-1">
                    <Skeleton className="h-8 w-16" />
                    <Skeleton className="h-8 w-16" />
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <Skeleton className="h-4 w-40" />
              </CardContent>
            </Card>
          ))}
        </div>
      ) : categories.length === 0 ? (
        <Card>
          <CardContent className="text-center py-12 text-gray-600">
            Nenhuma categoria criada. Crie sua primeira categoria!
          </CardContent>
        </Card>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {categories.map((category) => (
            <Card key={category.id}>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <div
                      className="w-4 h-4 rounded-full"
                      style={{ backgroundColor: category.color || "#gray" }}
                    ></div>
                    <CardTitle className="text-lg">{category.name}</CardTitle>
                  </div>
                  <div className="flex gap-1">
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleEdit(category)}
                    >
                      Editar
                    </Button>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleDelete(category.id, category.name)}
                      className="text-red-600 hover:text-red-700 hover:bg-red-50"
                    >
                      Deletar
                    </Button>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                {category.budget_limit && (
                  <div className="text-sm text-gray-600">
                    Limite mensal: {formatCurrency(category.budget_limit)}
                  </div>
                )}
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
