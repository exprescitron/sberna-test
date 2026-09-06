# Sběrna TEST — ověřovací doplněk do Outlooku

Nejmenší možný doplněk, který odpoví na jedinou otázku:
**dá se ve sdílené schránce `javex@javex.cz` přečíst zpráva, a hlavně její `conversationId`?**

Na tom stojí celý návrh Sběrny. Když to nejde, nemá smysl psát nic dalšího.

Doplněk **jen čte**. Neodesílá poštu, nikam nic neukládá, nevolá žádnou další službu.

---

## Krok 0 — nejlevnější kontrola, udělej ji první

Microsoft dokumentuje, že **u schránky skryté z globálního adresáře je
`Office.context.mailbox.item` vždy `null`** — doplněk se načte, ale nic nepřečte.

Ověř v Microsoft 365 admin centru:

**Teams a skupiny → Sdílené poštovní schránky → javex@javex.cz**
→ volba *Skrýt z globálního seznamu adres* musí být **vypnutá**.

Přes PowerShell:

```powershell
Get-Mailbox javex@javex.cz | Select-Object HiddenFromAddressListsEnabled
# musí vrátit False
```

Když vrátí `True` a nechceš to měnit, dál nepokračuj — návrh v téhle podobě neprojde.

---

## Krok 1 — vystavit soubory na HTTPS

Doplněk musí být dostupný přes HTTPS. Nejrychleji přes GitHub Pages.

1. Na GitHubu založ **veřejný** repozitář `sberna-test` pod účtem `exprescitron`
   *(veřejný proto, že Pages na privátním repozitáři vyžadují placený tarif;
   v těchto souborech nejsou žádná hesla ani firemní data)*
2. Nahraj do něj obsah této složky
3. **Settings → Pages → Source: Deploy from a branch → main → / (root)**
4. Za pár minut ověř v prohlížeči:
   `https://exprescitron.github.io/sberna-test/taskpane.html`
   Musí se objevit panel s nadpisem „Sběrna TEST".

> Pokud repozitář pojmenuješ jinak nebo použiješ jiný hosting,
> je nutné přepsat **všechny URL v `manifest.xml`**. Jsou tam na sedmi místech.

---

## Krok 2 — nasadit doplněk jen na sebe

**Microsoft 365 admin centrum → Nastavení → Integrované aplikace
→ Nahrát vlastní aplikace**

- Typ: *Doplněk Office (manifest)*
- Nahraj `manifest.xml`
- Přiřadit: **Konkrétní uživatelé → jen Tomáš Lukšík**

Nasazení může trvat i několik hodin, než se doplněk objeví. Obvykle je to do hodiny.

---

## Krok 3 — test

1. V **novém Outlooku** otevři zprávu ve schránce `javex@javex.cz`
2. V liště nad zprávou klikni na **Sběrna TEST**
3. Nahoře v panelu bude jeden ze tří výsledků:

| Výsledek | Co to znamená |
|---|---|
| **FUNGUJE** | zpráva se čte včetně `conversationId` — návrh Sběrny je průchozí |
| **ZPRÁVA SE NEČTE** | `item` je `null` — skoro jistě ta skrytá schránka z kroku 0 |
| **NEFUNGUJE** | doplněk se vůbec nespustil — chyba v nasazení nebo regrese v klientovi |

4. Zmáčkni **Zkopírovat výsledek** a pošli mi ho.

Zopakuj to celé ještě jednou nad zprávou ve **vlastní** schránce `luksik@javex.cz`.
Rozdíl mezi těmi dvěma výsledky je přesně to, co potřebuju vidět.

---

## Co je v manifestu důležité

```xml
<SupportsSharedFolders>true</SupportsSharedFolders>
```

Výchozí hodnota je `false`. **Bez tohoto řádku se tlačítko ve sdílené schránce
vůbec nezobrazí** — a je to nejčastější důvod, proč lidem doplňky ve sdílených
schránkách „nefungují".

Oprávnění je nastavené na `ReadItem`, tedy nejnižší možné.

---

## Soubory

| Soubor | K čemu |
|---|---|
| `manifest.xml` | popis doplňku pro Outlook — tohle se nahrává do admin centra |
| `taskpane.html` | samotný panel, včetně veškeré logiky |
| `commands.html` | prázdný, vyžaduje ho schéma manifestu |
| `index.html` | úvodní stránka, jen aby odkaz v manifestu někam vedl |
| `assets/icon-*.png` | ikony tlačítka |
