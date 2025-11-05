"use client";

import { useState, useEffect } from "react";
import { useAuth } from "@/lib/auth-context";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

interface Projection {
  id: string;
  name: string;
  description?: string;
  start_date?: string;
  end_date?: string;
  total_transactions: number;
  total_income: number;
  total_expenses: number;
  balance: number;
}

export default function ProjectionsPage() {
  const { token } = useAuth();
  const [projections, setProjections] = useState<Projection[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadProjections();
  }, []);

  const loadProjections = async () => {
    if (!token) return;

    try {
      setLoading(true);
      const response = await fetch("http://localhost:8000/api/projections", {
        headers: { Authorization: `Bearer ${token}` },
      });
      const data = await response.json();
      setProjections(data);
    } catch (error) {
      console.error("Erro ao carregar projeções:", error);
    } finally {
      setLoading(false);
    }
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat("pt-BR", {
      style: "currency",
      currency: "BRL",
    }).format(value);
  };

  const handleCreateProjection = async () => {
    if (!token) return;

    const name = prompt("Nome do cenário de projeção:");
    if (!name) return;

    try {
      await fetch("http://localhost:8000/api/projections", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name,
          description: "Cenário criado manualmente",
          is_active: true,
        }),
      });

      loadProjections();
    } catch (error: any) {
      alert("Erro ao criar projeção: " + error.message);
    }
  };

  const handleDelete = async (id: string) => {
    if (!token) return;
    if (!confirm("Deseja realmente deletar este cenário?")) return;

    try {
      await fetch(`http://localhost:8000/api/projections/${id}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });

      loadProjections();
    } catch (error: any) {
      alert("Erro ao deletar: " + error.message);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">Projeções Manuais</h2>
          <p className="text-gray-600">
            Crie cenários "what-if" e simule diferentes situações financeiras
          </p>
        </div>
        <Button onClick={handleCreateProjection}>Novo Cenário</Button>
      </div>

      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h3 className="font-medium text-blue-900 mb-2">💡 O que são Projeções?</h3>
        <p className="text-sm text-blue-800">
          As projeções permitem criar cenários isolados dos seus dados reais. Você pode
          adicionar transações fictícias para simular situações como "E se eu comprasse
          um carro?" ou "Como ficaria meu orçamento com 20% menos gastos?". Essas
          simulações não afetam seus dados reais.
        </p>
      </div>

      {loading ? (
        <div className="text-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900 mx-auto"></div>
          <p className="mt-2 text-gray-600">Carregando...</p>
        </div>
      ) : projections.length === 0 ? (
        <Card>
          <CardContent className="text-center py-12 text-gray-600">
            Nenhum cenário criado. Crie seu primeiro cenário de projeção!
          </CardContent>
        </Card>
      ) : (
        <div className="grid gap-4 md:grid-cols-2">
          {projections.map((projection) => (
            <Card key={projection.id}>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle>{projection.name}</CardTitle>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => handleDelete(projection.id)}
                    className="text-red-600"
                  >
                    Deletar
                  </Button>
                </div>
                {projection.description && (
                  <CardDescription>{projection.description}</CardDescription>
                )}
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Transações:</span>
                    <span className="font-medium">{projection.total_transactions}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Receitas:</span>
                    <span className="font-medium text-green-600">
                      {formatCurrency(projection.total_income)}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Despesas:</span>
                    <span className="font-medium text-red-600">
                      {formatCurrency(projection.total_expenses)}
                    </span>
                  </div>
                  <div className="flex justify-between pt-2 border-t">
                    <span className="font-medium">Saldo:</span>
                    <span
                      className={`font-bold ${
                        projection.balance >= 0 ? "text-green-600" : "text-red-600"
                      }`}
                    >
                      {formatCurrency(projection.balance)}
                    </span>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
