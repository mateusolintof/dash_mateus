"use client";

import { useState } from "react";
import { useAuth } from "@/lib/auth-context";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { toast } from "sonner";

interface ParsedTransaction {
  temp_id: number;
  date: string;
  description: string;
  amount: number;
  suggested_category?: string;
  selected_category_id?: string;
}

export default function UploadPage() {
  const { token } = useAuth();
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [transactions, setTransactions] = useState<ParsedTransaction[]>([]);
  const [categories, setCategories] = useState<any[]>([]);
  const [bankStatementId, setBankStatementId] = useState<string>("");
  const [step, setStep] = useState<"upload" | "review">("upload");

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file || !token) return;

    setUploading(true);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch("http://localhost:8000/api/upload/statement", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Erro ao fazer upload");
      }

      const data = await response.json();

      setTransactions(data.transactions);
      setCategories(data.available_categories);
      setBankStatementId(data.bank_statement_id);
      setStep("review");
      toast.success(`${data.total_transactions} transações encontradas!`);
    } catch (error: any) {
      toast.error("Erro ao processar extrato: " + error.message);
    } finally {
      setUploading(false);
    }
  };

  const handleCategoryChange = (tempId: number, categoryName: string) => {
    setTransactions((prev) =>
      prev.map((trans) =>
        trans.temp_id === tempId
          ? { ...trans, suggested_category: categoryName }
          : trans
      )
    );
  };

  const handleConfirm = async () => {
    if (!token) return;

    setUploading(true);

    try {
      const transactionsToSave = transactions.map((trans) => ({
        date: trans.date,
        description: trans.description,
        amount: trans.amount,
        category_id: null, // Simplificado - você pode mapear categoria por nome
      }));

      const response = await fetch(
        `http://localhost:8000/api/upload/statement/${bankStatementId}/confirm`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            bank_statement_id: bankStatementId,
            transactions: transactionsToSave,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Erro ao confirmar transações");
      }

      toast.success("Transações importadas com sucesso!");

      // Reset
      setFile(null);
      setTransactions([]);
      setStep("upload");
    } catch (error: any) {
      toast.error("Erro ao confirmar: " + error.message);
    } finally {
      setUploading(false);
    }
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat("pt-BR", {
      style: "currency",
      currency: "BRL",
    }).format(value);
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString + "T00:00:00").toLocaleDateString("pt-BR");
  };

  if (step === "review") {
    return (
      <div className="space-y-6">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">Revisar Transações</h2>
          <p className="text-gray-600">
            Revise as transações e ajuste as categorias antes de confirmar
          </p>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>{transactions.length} transações encontradas</CardTitle>
            <CardDescription>
              A IA sugeriu categorias automaticamente. Você pode ajustá-las antes de
              confirmar.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3 max-h-[500px] overflow-y-auto">
              {transactions.map((trans) => (
                <div
                  key={trans.temp_id}
                  className="flex items-center justify-between border rounded-lg p-3 hover:bg-gray-50"
                >
                  <div className="flex-1">
                    <p className="font-medium">{trans.description}</p>
                    <p className="text-sm text-gray-500">{formatDate(trans.date)}</p>
                  </div>
                  <div className="flex items-center gap-4">
                    <span
                      className={`font-semibold ${
                        trans.amount >= 0 ? "text-green-600" : "text-red-600"
                      }`}
                    >
                      {formatCurrency(trans.amount)}
                    </span>
                    <select
                      value={trans.suggested_category || ""}
                      onChange={(e) =>
                        handleCategoryChange(trans.temp_id, e.target.value)
                      }
                      className="border rounded px-3 py-1 text-sm"
                    >
                      <option value="">Sem categoria</option>
                      {categories.map((cat) => (
                        <option key={cat} value={cat}>
                          {cat}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>
              ))}
            </div>

            <div className="flex gap-3 mt-6">
              <Button
                variant="outline"
                onClick={() => {
                  setStep("upload");
                  setTransactions([]);
                  setFile(null);
                }}
              >
                Cancelar
              </Button>
              <Button onClick={handleConfirm} disabled={uploading} className="flex-1">
                {uploading ? "Confirmando..." : "Confirmar e Importar"}
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold tracking-tight">Upload de Extrato</h2>
        <p className="text-gray-600">
          Importe suas transações a partir de um extrato bancário
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardHeader>
            <div className="text-3xl mb-2">📄</div>
            <CardTitle>1. Selecione o arquivo</CardTitle>
            <CardDescription>Formato CSV do seu banco</CardDescription>
          </CardHeader>
        </Card>

        <Card>
          <CardHeader>
            <div className="text-3xl mb-2">🤖</div>
            <CardTitle>2. IA Categoriza</CardTitle>
            <CardDescription>Automático e inteligente</CardDescription>
          </CardHeader>
        </Card>

        <Card>
          <CardHeader>
            <div className="text-3xl mb-2">✅</div>
            <CardTitle>3. Você Revisa</CardTitle>
            <CardDescription>E confirma a importação</CardDescription>
          </CardHeader>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Fazer Upload</CardTitle>
          <CardDescription>
            Selecione um arquivo CSV exportado do seu banco
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="file">Arquivo CSV</Label>
            <Input
              id="file"
              type="file"
              accept=".csv"
              onChange={handleFileChange}
              disabled={uploading}
            />
            {file && (
              <p className="text-sm text-gray-600">
                Arquivo selecionado: {file.name} ({(file.size / 1024).toFixed(2)} KB)
              </p>
            )}
          </div>

          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h4 className="font-medium text-blue-900 mb-2">💡 Dicas:</h4>
            <ul className="text-sm text-blue-800 space-y-1">
              <li>• O arquivo deve estar no formato CSV</li>
              <li>• Deve conter colunas: Data, Descrição e Valor</li>
              <li>• Formatos suportados: Nubank, Inter, Itaú, C6 Bank</li>
              <li>• A IA irá categorizar automaticamente cada transação</li>
            </ul>
          </div>

          <Button
            onClick={handleUpload}
            disabled={!file || uploading}
            className="w-full"
          >
            {uploading ? "Processando..." : "Fazer Upload e Processar"}
          </Button>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Bancos Suportados</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {["Nubank", "Banco Inter", "Itaú", "C6 Bank", "Bradesco", "Santander", "Caixa", "Outros"].map(
              (bank) => (
                <div
                  key={bank}
                  className="text-center py-3 px-4 border rounded-lg hover:bg-gray-50"
                >
                  {bank}
                </div>
              )
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
