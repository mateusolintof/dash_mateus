"use client";

import { useState } from "react";
import { useAuth } from "@/lib/auth-context";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { toast } from "sonner";

export default function SettingsPage() {
  const { user } = useAuth();
  const [loading, setLoading] = useState(false);

  const [profileData, setProfileData] = useState({
    name: user?.name || "",
    email: user?.email || "",
  });

  const [passwordData, setPasswordData] = useState({
    current: "",
    new: "",
    confirm: "",
  });

  const handleProfileUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    // Simula update (endpoint não implementado no backend)
    await new Promise(resolve => setTimeout(resolve, 1000));

    toast.success("Perfil atualizado! (Simulado - endpoint não implementado)");
    setLoading(false);
  };

  const handlePasswordUpdate = async (e: React.FormEvent) => {
    e.preventDefault();

    if (passwordData.new !== passwordData.confirm) {
      toast.error("As senhas não coincidem!");
      return;
    }

    if (passwordData.new.length < 6) {
      toast.error("Senha deve ter pelo menos 6 caracteres!");
      return;
    }

    setLoading(true);

    // Simula update
    await new Promise(resolve => setTimeout(resolve, 1000));

    toast.success("Senha atualizada! (Simulado - endpoint não implementado)");
    setPasswordData({ current: "", new: "", confirm: "" });
    setLoading(false);
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold tracking-tight">Configurações</h2>
        <p className="text-gray-600">Gerencie suas preferências e conta</p>
      </div>

      <div className="grid gap-6">
        {/* Perfil */}
        <Card>
          <CardHeader>
            <CardTitle>Perfil</CardTitle>
            <CardDescription>
              Atualize suas informações pessoais
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleProfileUpdate} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="name">Nome</Label>
                <Input
                  id="name"
                  value={profileData.name}
                  onChange={(e) =>
                    setProfileData({ ...profileData, name: e.target.value })
                  }
                  placeholder="Seu nome"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  value={profileData.email}
                  disabled
                  className="bg-gray-100"
                />
                <p className="text-xs text-gray-500">
                  Email não pode ser alterado
                </p>
              </div>

              <Button type="submit" disabled={loading}>
                {loading ? "Salvando..." : "Salvar Alterações"}
              </Button>
            </form>
          </CardContent>
        </Card>

        {/* Senha */}
        <Card>
          <CardHeader>
            <CardTitle>Alterar Senha</CardTitle>
            <CardDescription>
              Atualize sua senha de acesso
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handlePasswordUpdate} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="current">Senha Atual</Label>
                <Input
                  id="current"
                  type="password"
                  value={passwordData.current}
                  onChange={(e) =>
                    setPasswordData({ ...passwordData, current: e.target.value })
                  }
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="new">Nova Senha</Label>
                <Input
                  id="new"
                  type="password"
                  value={passwordData.new}
                  onChange={(e) =>
                    setPasswordData({ ...passwordData, new: e.target.value })
                  }
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="confirm">Confirmar Nova Senha</Label>
                <Input
                  id="confirm"
                  type="password"
                  value={passwordData.confirm}
                  onChange={(e) =>
                    setPasswordData({ ...passwordData, confirm: e.target.value })
                  }
                  required
                />
              </div>

              <Button type="submit" disabled={loading}>
                {loading ? "Atualizando..." : "Atualizar Senha"}
              </Button>
            </form>
          </CardContent>
        </Card>

        {/* Preferências */}
        <Card>
          <CardHeader>
            <CardTitle>Preferências</CardTitle>
            <CardDescription>
              Ajuste como o sistema funciona
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="font-medium">Notificações de Orçamento</p>
                <p className="text-sm text-gray-500">
                  Receber avisos quando atingir limite de categoria
                </p>
              </div>
              <Button variant="outline" size="sm">
                Em Breve
              </Button>
            </div>

            <div className="flex items-center justify-between">
              <div>
                <p className="font-medium">Tema Escuro</p>
                <p className="text-sm text-gray-500">
                  Ativar modo escuro no dashboard
                </p>
              </div>
              <Button variant="outline" size="sm">
                Em Breve
              </Button>
            </div>

            <div className="flex items-center justify-between">
              <div>
                <p className="font-medium">Exportar Dados</p>
                <p className="text-sm text-gray-500">
                  Baixar todas as suas transações em CSV
                </p>
              </div>
              <Button variant="outline" size="sm">
                Em Breve
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Conta */}
        <Card>
          <CardHeader>
            <CardTitle>Conta</CardTitle>
            <CardDescription>
              Informações sobre sua conta
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <p className="text-sm text-gray-600">
                Membro desde: {new Date().toLocaleDateString("pt-BR")}
              </p>
            </div>

            <div className="pt-4 border-t">
              <Button
                variant="destructive"
                onClick={() => {
                  if (confirm("Deseja realmente deletar sua conta? Esta ação é irreversível!")) {
                    toast.error("Funcionalidade não implementada");
                  }
                }}
              >
                Deletar Conta
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
