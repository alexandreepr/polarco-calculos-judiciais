import uuid
from datetime import date
from typing import Optional, List, Dict
from pydantic import BaseModel, ConfigDict, Field

class LegalCaseBase(BaseModel):
    legal_case_number: str
    case_subject: Optional[str] = None
    state: Optional[str] = None
    jurisdiction: Optional[str] = None
    judicial_district: Optional[str] = None
    court: Optional[str] = None
    defendant: Optional[str] = None
    attorney: Optional[str] = None
    clients: Optional[List[Dict[str, str]]] = None  # List of dicts with name/cpf
    status: Optional[str] = None

    assignee_from_juridical_team_id: Optional[uuid.UUID] = None
    assignee_from_litigation_team_id: Optional[uuid.UUID] = None

    # juridical dates
    filing_date: Optional[date] = None                    # DATA DE AJUIZAMENTO
    final_judgment_date: Optional[date] = None            # DATA DO TRÂNSITO EM JULGADO
    citation_date: Optional[date] = None                  # DATA DA CITAÇÃO
    damage_event_date: Optional[date] = None              # DATA DO EVENTO DANOSO
    judgment_date: Optional[date] = None                  # DATA DA SENTENÇA
    appellate_decision_date: Optional[date] = None        # DATA DO ACÓRDÃO

    # moral (non-pecuniary) damage
    nominal_moral_damage: Optional[float] = None          # VALOR DOS DANOS MORAIS
    moral_index_start_date: Optional[date] = None         # ATUALIZAÇÃO A PARTIR (DANOS MORAIS)
    moral_interest_start_date: Optional[date] = None      # JUROS A PARTIR (DANOS MORAIS)
    moral_index_type: Optional[str] = None                # INDICE ATUALIZAÇAO DANOS MORAIS (MonetaryIndexType)
    moral_interest_index_type: Optional[str] = None       # INDICE JUROS DANOS MORAIS (InterestIndexType)
    moral_end_date: Optional[date] = None

    # material (pecuniary) damage
    nominal_material_damage: Optional[float] = None       # VALOR DOS DANOS MATERIAIS
    material_index_start_date: Optional[date] = None      # ATUALIZAÇÃO A PARTIR (DANOS MATERIAIS)
    material_interest_start_date: Optional[date] = None   # JUROS A PARTIR (DANOS MATERIAIS)
    material_index_type: Optional[str] = None             # INDICE ATUALIZAÇAO DANOS MATERIAIS
    material_interest_index_type: Optional[str] = None    # INDICE JUROS DANOS MATERIAIS
    material_end_date: Optional[date] = None

    # material installments / resolution
    first_installment_date: Optional[date] = None         # DATA DA PRIMEIRA PARCELA
    last_installment_date: Optional[date] = None          # DATA DA ÚLTIMA PARCELA
    first_installment_amount: Optional[float] = None      # VALOR DA PRIMEIRA PARCELA
    last_installment_amount: Optional[float] = None       # VALOR DA ÚLTIMA PARCELA
    material_resolution: Optional[str] = None             # ANULADO / CONVERTIDO
    material_interest_multiplier: Optional[str] = None    # SIMPLES / DOBRADO

    # case value basis (three-option) and fees (already present above but keep for clarity)
    case_value_basis: Optional[str] = None                            # CONDEMNATION_AMOUNT / CLAIM_AMOUNT / SPECIFIED_AMOUNT
    case_value: Optional[float] = None                                # VALOR DA CAUSA
    attorney_fees_value: Optional[float] = None                       # VALOR DOS HONORÁRIOS ADVOCATÍCIOS
    percentage_contractual_attorney_fees: Optional[float] = None      # PERCENTUAL DOS HONORÁRIOS CONTRATUAIS
    percentage_court_awarded_attorney_fees: Optional[float] = None    # PERCENTUAL DOS HONORÁRIOS CONCEDIDOS
    proportion_court_awarded_attorney_fees: Optional[float] = None    # PROPORÇÃO DOS HONORÁRIOS CONCEDIDOS

class LegalCaseCreate(LegalCaseBase):
    pass

class LegalCaseUpdate(LegalCaseBase):
    pass

class LegalCaseResponse(LegalCaseBase):
    id: uuid.UUID = Field(...)
    model_config = ConfigDict(from_attributes=True)