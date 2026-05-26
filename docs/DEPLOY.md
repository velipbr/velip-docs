# Publicação — developers.velip.com.br

Este repositório publica a documentação via **GitHub Pages** na pasta `/docs`, com domínio customizado `developers.velip.com.br`.

## Pré-requisitos no repositório

Já incluídos em `docs/`:

| Arquivo | Função |
| --- | --- |
| `CNAME` | Aponta o domínio customizado |
| `_config.yml` | Tema Jekyll (GitHub Pages) |
| `index.md` | Landing page em `/` |

## 1. Habilitar GitHub Pages

1. Abra [github.com/velipbr/velip-docs/settings/pages](https://github.com/velipbr/velip-docs/settings/pages)
2. **Source:** Deploy from a branch
3. **Branch:** `main` — folder **`/docs`**
4. **Custom domain:** `developers.velip.com.br`
5. Aguarde a validação DNS (pode levar até 24 h)
6. Marque **Enforce HTTPS** assim que o certificado Let's Encrypt estiver ativo

## 2. Configurar DNS

Na zona DNS de `velip.com.br`, crie:

| Tipo | Nome | Valor | TTL |
| --- | --- | --- | --- |
| CNAME | `developers` | `velipbr.github.io` | 3600 |

> Se o registrador não permitir CNAME na raiz de um subdomínio, use o painel do provedor de DNS (Cloudflare, Route53, etc.) conforme a documentação do GitHub Pages.

## 3. Validar

Após propagação DNS e deploy:

```bash
curl -I https://developers.velip.com.br/
curl -I https://developers.velip.com.br/mcp/overview
```

URLs esperadas:

- Home: `https://developers.velip.com.br/`
- API v2: `https://developers.velip.com.br/api/v2/overview`
- MCP: `https://developers.velip.com.br/mcp/overview`

## 4. Atualizações

Cada push na branch `main` atualiza o site automaticamente em ~1 minuto.
