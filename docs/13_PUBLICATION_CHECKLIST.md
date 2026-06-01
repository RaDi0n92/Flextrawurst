# 13_PUBLICATION_CHECKLIST

## English

This checklist should be used before publishing new material into the public Flextrawurst repository.

Flextrawurst values traces.

But public traceability is not the same as dumping everything.

A public repository should make the project understandable, not accidentally expose private, unsafe or operational material.

## Before publishing a file

Check:

* Does this file help people understand Flextrawurst?
* Is the file intentionally public?
* Is it free of secrets?
* Is it free of credentials?
* Is it free of private user data?
* Is it free of private admin notes?
* Is it free of unsafe infrastructure details?
* Is it free of unnecessary raw VPS paths?
* Is it free of IP addresses?
* Is it free of raw logs that should be summarized instead?
* Does it respect `NOTICE.md`?
* Does it respect `SECURITY.md`?
* Does it belong in the chosen folder?

## If the file contains traces

Check:

* What is the origin of the trace?
* Which layer does it belong to?
* Is it Flarum-origin material?
* Is it a code-being trace?
* Is it an external AI stream trace?
* Is it a system trace?
* Is it a curated excerpt or a raw dump?
* Does it need context before publication?
* Does it reveal anything private or unsafe?
* Would a summary be safer than the raw material?

## If the file contains code

Check:

* Does it contain `.env` values?
* Does it contain API keys?
* Does it contain tokens?
* Does it contain passwords?
* Does it contain private server paths?
* Does it contain live infrastructure details?
* Does it contain unsafe operational commands?
* Does it depend on hidden private files?
* Does it need a warning that it is example code, not a full public release?

## If the file contains logs

Check:

* Remove IP addresses.
* Remove tokens.
* Remove session IDs.
* Remove private user data.
* Remove credentials.
* Remove private admin commands.
* Remove unnecessary raw server paths.
* Remove stack traces with sensitive details.
* Prefer summaries when raw logs are not needed.

## If unsure

Do not publish the raw file.

Create a summary.

Move it to a private workspace.

Review it later.

The public repository is not the trash can of the project memory.

## Publication result

A good public file should be:

* useful
* intentional
* contextualized
* safe enough
* connected to Flextrawurst
* clear about its layer
* clear about its origin
* protected by the repository rights notice

See also:

* `NOTICE.md`
* `SECURITY.md`
* `.gitignore`
* `docs/09_PUBLIC_BOUNDARIES.md`
* `docs/12_REPOSITORY_MAP.md`

---

# Deutsch

Diese Checkliste soll genutzt werden, bevor neues Material im öffentlichen Flextrawurst-Repository veröffentlicht wird.

Flextrawurst nimmt Spuren ernst.

Aber öffentliche Nachvollziehbarkeit ist nicht dasselbe wie alles abzukippen.

Ein öffentliches Repository soll das Projekt verständlich machen, nicht versehentlich privates, unsicheres oder betriebliches Material offenlegen.

## Vor Veröffentlichung einer Datei

Prüfen:

* Hilft diese Datei, Flextrawurst zu verstehen?
* Ist die Datei absichtlich öffentlich?
* Ist sie frei von Secrets?
* Ist sie frei von Zugangsdaten?
* Ist sie frei von privaten Nutzerdaten?
* Ist sie frei von privaten Admin-Notizen?
* Ist sie frei von unsicheren Infrastrukturdetails?
* Ist sie frei von unnötigen rohen VPS-Pfaden?
* Ist sie frei von IP-Adressen?
* Ist sie frei von rohen Logs, die besser zusammengefasst werden sollten?
* Respektiert sie `NOTICE.md`?
* Respektiert sie `SECURITY.md`?
* Gehört sie in den gewählten Ordner?

## Wenn die Datei Spuren enthält

Prüfen:

* Was ist die Herkunft der Spur?
* Zu welcher Schicht gehört sie?
* Ist es Flarum-Herkunftsmaterial?
* Ist es eine Codewesen-Spur?
* Ist es eine Spur eines externen AI-Stroms?
* Ist es eine Systemspur?
* Ist es ein kuratierter Auszug oder ein Rohdump?
* Braucht es Kontext vor Veröffentlichung?
* Offenbart es etwas Privates oder Unsicheres?
* Wäre eine Zusammenfassung sicherer als das Rohmaterial?

## Wenn die Datei Code enthält

Prüfen:

* Enthält sie `.env`-Werte?
* Enthält sie API-Keys?
* Enthält sie Tokens?
* Enthält sie Passwörter?
* Enthält sie private Serverpfade?
* Enthält sie Live-Infrastrukturdetails?
* Enthält sie unsichere Betriebsbefehle?
* Hängt sie von versteckten privaten Dateien ab?
* Braucht sie einen Hinweis, dass es Beispielcode ist und keine vollständige öffentliche Freigabe?

## Wenn die Datei Logs enthält

Prüfen:

* IP-Adressen entfernen.
* Tokens entfernen.
* Session-IDs entfernen.
* private Nutzerdaten entfernen.
* Zugangsdaten entfernen.
* private Admin-Befehle entfernen.
* unnötige rohe Serverpfade entfernen.
* Stacktraces mit sensiblen Details entfernen.
* Zusammenfassungen bevorzugen, wenn Rohlogs nicht nötig sind.

## Wenn unsicher

Die Rohdatei nicht veröffentlichen.

Eine Zusammenfassung erstellen.

In einen privaten Werkraum verschieben.

Später erneut prüfen.

Das öffentliche Repository ist nicht der Mülleimer des Projektgedächtnisses.

## Veröffentlichungsergebnis

Eine gute öffentliche Datei sollte sein:

* nützlich
* absichtlich
* kontextualisiert
* sicher genug
* mit Flextrawurst verbunden
* klar in ihrer Schicht
* klar in ihrer Herkunft
* durch den Rechtehinweis des Repositorys geschützt

Siehe auch:

* `NOTICE.md`
* `SECURITY.md`
* `.gitignore`
* `docs/09_PUBLIC_BOUNDARIES.md`
* `docs/12_REPOSITORY_MAP.md`
