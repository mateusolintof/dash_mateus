import pandas as pd
from typing import List, Dict, Optional
from datetime import datetime
from io import StringIO, BytesIO
import csv


class BankStatementParser:
    """Parser para extratos bancários em diferentes formatos"""

    @staticmethod
    def parse_csv(file_content: bytes, encoding: str = "utf-8") -> List[Dict]:
        """
        Parse de extrato CSV genérico.

        Formato esperado (colunas podem variar):
        - Data
        - Descrição/Histórico
        - Valor/Débito/Crédito

        Args:
            file_content: Conteúdo do arquivo CSV em bytes
            encoding: Encoding do arquivo (padrão utf-8, bancos BR: latin1)

        Returns:
            Lista de transações parseadas
        """
        try:
            # Tentar diferentes encodings
            encodings = [encoding, "utf-8", "latin1", "iso-8859-1"]
            df = None

            for enc in encodings:
                try:
                    content_str = file_content.decode(enc)
                    df = pd.read_csv(StringIO(content_str))
                    break
                except:
                    continue

            if df is None:
                raise ValueError("Não foi possível decodificar o arquivo CSV")

            transactions = []

            # Normalizar nomes de colunas (lowercase, sem espaços)
            df.columns = df.columns.str.lower().str.strip()

            # Detectar colunas de data, descrição e valor
            date_col = BankStatementParser._find_column(
                df, ["data", "date", "dt"]
            )
            desc_col = BankStatementParser._find_column(
                df, ["descricao", "descrição", "historico", "histórico", "description"]
            )
            value_col = BankStatementParser._find_column(
                df, ["valor", "value", "amount"]
            )

            # Se não encontrou valor único, pode ter débito/crédito separados
            debit_col = BankStatementParser._find_column(
                df, ["debito", "débito", "debit", "saida", "saída"]
            )
            credit_col = BankStatementParser._find_column(
                df, ["credito", "crédito", "credit", "entrada"]
            )

            for _, row in df.iterrows():
                try:
                    # Parse da data
                    date_str = str(row[date_col])
                    date_obj = BankStatementParser._parse_date(date_str)

                    # Descrição
                    description = str(row[desc_col]).strip()

                    # Valor
                    if value_col:
                        amount = BankStatementParser._parse_amount(str(row[value_col]))
                    elif debit_col and credit_col:
                        debit = BankStatementParser._parse_amount(str(row[debit_col]))
                        credit = BankStatementParser._parse_amount(str(row[credit_col]))
                        amount = credit - debit
                    else:
                        continue

                    if date_obj and description and amount != 0:
                        transactions.append({
                            "date": date_obj.strftime("%Y-%m-%d"),
                            "description": description,
                            "amount": float(amount)
                        })

                except Exception as e:
                    print(f"Erro ao processar linha: {e}")
                    continue

            return transactions

        except Exception as e:
            raise ValueError(f"Erro ao fazer parse do CSV: {str(e)}")

    @staticmethod
    def _find_column(df: pd.DataFrame, possible_names: List[str]) -> Optional[str]:
        """Encontra coluna por nomes possíveis"""
        for col in df.columns:
            if any(name in col.lower() for name in possible_names):
                return col
        return None

    @staticmethod
    def _parse_date(date_str: str) -> Optional[datetime]:
        """Parse de data em vários formatos"""
        formats = [
            "%d/%m/%Y",
            "%Y-%m-%d",
            "%d-%m-%Y",
            "%d/%m/%y",
            "%Y/%m/%d",
        ]

        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except:
                continue

        return None

    @staticmethod
    def _parse_amount(value_str: str) -> float:
        """Parse de valor monetário"""
        if not value_str or value_str.lower() in ['nan', 'none', '']:
            return 0.0

        # Remover símbolos de moeda e espaços
        value_str = value_str.replace("R$", "").replace("$", "").strip()

        # Substituir vírgula por ponto (formato BR)
        value_str = value_str.replace(".", "").replace(",", ".")

        # Remover outros caracteres não numéricos (exceto - e .)
        value_str = ''.join(c for c in value_str if c.isdigit() or c in ['-', '.'])

        try:
            return float(value_str)
        except:
            return 0.0

    @staticmethod
    def detect_bank(file_content: bytes) -> Optional[str]:
        """
        Tenta detectar o banco pelo formato do CSV.
        Retorna: 'nubank', 'inter', 'itau', 'generic', etc.
        """
        try:
            content_str = file_content.decode('utf-8', errors='ignore')
            first_lines = content_str[:500].lower()

            if 'nubank' in first_lines:
                return 'nubank'
            elif 'inter' in first_lines or 'banco inter' in first_lines:
                return 'inter'
            elif 'itau' in first_lines or 'itaú' in first_lines:
                return 'itau'
            elif 'bradesco' in first_lines:
                return 'bradesco'
            elif 'santander' in first_lines:
                return 'santander'

            return 'generic'

        except:
            return 'generic'


# Instância global
parser_service = BankStatementParser()
