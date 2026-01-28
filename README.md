# Leipzig Book Fair 2026 - Scraper de Expositores

## 📋 Objetivo
Extrair dados de contato de todos os 1.397 expositores da Leipzig Book Fair 2026.

## 📊 Dados Extraídos
- Nome do Expositor
- País
- Pessoa de Contato
- Email
- Telefone
- Website
- Endereço
- Hall/Stand
- URL do Perfil

## 🚀 Instalação

```bash
# Instalar dependências
pip install -r requirements.txt --break-system-packages

# Instalar Chrome Driver (Ubuntu)
sudo apt-get update
sudo apt-get install -y chromium-browser chromium-chromedriver
```

## ▶️ Como Usar

### Teste (20 expositores)
```python
python leipzig_scraper_full.py
```

### Produção (TODOS os 1.397)
Editar o arquivo e trocar:
```python
# Linha 165 - comentar:
# scraper.scrape_all(max_exhibitors=20)

# Linha 168 - descomentar:
scraper.scrape_all()
```

## ⏱️ Tempo Estimado
- 20 expositores: ~2-3 minutos
- 1.397 expositores: ~2-3 horas

## 📁 Output
- **Arquivo Excel**: `Leipzig_Book_Fair_2026_Exhibitors.xlsx`
- **Formato**: Pronto para envio/uso

## ⚠️ Observações
1. O site pode ter proteção anti-bot - ajustar delays se necessário
2. Nem todos expositores têm email/telefone públicos
3. Alguns dados podem estar em PDF/imagens (não extraídos)
4. Prazo da tarefa: **30 de janeiro de 2026**

## 🎯 Estratégia Alternativa
Se o scraping automático falhar:
1. Usar API do site (se disponível)
2. Contatar organização para lista oficial
3. Scraping manual com extensões de browser
4. Contratar serviço de data entry

## 📞 Melhorias Possíveis
- [ ] Adicionar retry automático em falhas
- [ ] Validar emails/telefones
- [ ] Buscar dados em redes sociais (LinkedIn)
- [ ] Adicionar progresso em tempo real
- [ ] Salvar checkpoints (retomar scraping)
