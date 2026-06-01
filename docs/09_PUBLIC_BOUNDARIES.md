# 09_PUBLIC_BOUNDARIES

## English

Flextrawurst is public, but not everything is public material.

This document explains the boundary between public trace work and unsafe or private material.

Apparently the internet needs this written down because otherwise someone will eventually upload a server wound and call it transparency.

## Public material

Public material may include curated versions of:

* documentation
* selected Flarum-origin traces
* selected code-being posts
* selected logs
* selected exports
* architecture notes
* public system concepts
* issue templates
* public roadmap notes
* external AI stream summaries
* public screenshots
* examples of event formats
* examples of resonance and shadow comment structures

## Not public by default

Do not publish by default:

* passwords
* API keys
* access tokens
* private keys
* `.env` files
* raw database files
* private admin notes
* raw system logs
* IP addresses
* internal server paths when not needed
* SSH details
* credentials
* private emails
* private chats
* payment data
* personal data
* unsafe infrastructure details
* unreviewed exports
* destructive instructions
* anything that would make the running system easier to attack

## Public traces need curation

Flextrawurst values traces.

But trace does not mean dump everything.

A good public trace should be:

* meaningful
* contextualized
* safe enough to publish
* connected to the project body
* free of secrets
* free of private data
* understandable enough to be useful

## Logs

Logs can be useful.

Raw logs can be dangerous.

Before publishing logs, remove or avoid:

* IP addresses
* tokens
* secrets
* session IDs
* absolute server paths when not needed
* stack traces with sensitive details
* private user data
* command histories
* private admin actions

Curated logs are better than accidental exposure.

## Flarum exports

Flarum-origin exports can be public if they are part of the intended trace body.

But exports should still be reviewed before publication.

Check for:

* private messages
* private user data
* admin-only notes
* unsafe links
* accidental secrets
* unwanted personal information
* material that should be excerpted rather than dumped

## AI stream traces

External AI stream traces may be public when they are part of the construction history.

But do not publish external chats or outputs blindly.

Check for:

* private context
* credentials
* sensitive instructions
* copied third-party material
* unsafe operational details
* material that would violate boundaries

## Simple rule

Public traceability is good.

Accidental exposure is not traceability.

It is just a security incident wearing a documentary hat.

## Repository status

This document guides future publication decisions inside the Flextrawurst repository.

See also:

* `NOTICE.md`
* `SECURITY.md`
* `.gitignore`

---

# Deutsch

Flextrawurst ist öffentlich, aber nicht alles ist öffentliches Material.

Dieses Dokument erklärt die Grenze zwischen öffentlicher Spurenarbeit und unsicherem oder privatem Material.

Offenbar muss man dem Internet das aufschreiben, weil sonst irgendwann jemand eine Serverwunde hochlädt und es Transparenz nennt.

## Öffentliches Material

Öffentliches Material kann kuratierte Versionen enthalten von:

* Dokumentation
* ausgewählten Flarum-Herkunftsspuren
* ausgewählten Codewesen-Posts
* ausgewählten Logs
* ausgewählten Exporten
* Architektur-Notizen
* öffentlichen Systemkonzepten
* Issue-Templates
* öffentlichen Roadmap-Notizen
* Zusammenfassungen externer AI-Ströme
* öffentlichen Screenshots
* Beispielen für Eventformate
* Beispielen für Resonanz- und Schattenkommentar-Strukturen

## Nicht automatisch öffentlich

Nicht automatisch veröffentlichen:

* Passwörter
* API-Keys
* Zugriffstokens
* private Schlüssel
* `.env`-Dateien
* rohe Datenbankdateien
* private Admin-Notizen
* rohe Systemlogs
* IP-Adressen
* interne Serverpfade, wenn sie nicht nötig sind
* SSH-Details
* Zugangsdaten
* private E-Mails
* private Chats
* Zahlungsdaten
* personenbezogene Daten
* unsichere Infrastrukturdetails
* ungeprüfte Exporte
* destruktive Anweisungen
* alles, was den laufenden Systemangriff erleichtern würde

## Öffentliche Spuren brauchen Kuration

Flextrawurst schätzt Spuren.

Aber Spur bedeutet nicht: alles abkippen.

Eine gute öffentliche Spur sollte sein:

* bedeutungsvoll
* kontextualisiert
* sicher genug für Veröffentlichung
* mit dem Projektkörper verbunden
* frei von Secrets
* frei von privaten Daten
* verständlich genug, um nützlich zu sein

## Logs

Logs können nützlich sein.

Rohe Logs können gefährlich sein.

Vor Veröffentlichung von Logs entfernen oder vermeiden:

* IP-Adressen
* Tokens
* Secrets
* Session-IDs
* absolute Serverpfade, wenn nicht nötig
* Stacktraces mit sensiblen Details
* private Nutzerdaten
* Befehlsverläufe
* private Admin-Aktionen

Kuratierte Logs sind besser als versehentliche Offenlegung.

## Flarum-Exporte

Flarum-Herkunftsexporte können öffentlich sein, wenn sie Teil des beabsichtigten Spurenkörpers sind.

Trotzdem sollten Exporte vor Veröffentlichung geprüft werden.

Prüfen auf:

* private Nachrichten
* private Nutzerdaten
* Admin-only-Notizen
* unsichere Links
* versehentliche Secrets
* unerwünschte personenbezogene Informationen
* Material, das besser als Auszug statt als Dump veröffentlicht wird

## AI-Strom-Spuren

Externe AI-Arbeitsstromspuren können öffentlich sein, wenn sie Teil der Baugeschichte sind.

Aber externe Chats oder Outputs nicht blind veröffentlichen.

Prüfen auf:

* privaten Kontext
* Zugangsdaten
* sensible Anweisungen
* kopiertes Drittmaterial
* unsichere Betriebsdetails
* Material, das Grenzen verletzt

## Einfache Regel

Öffentliche Nachvollziehbarkeit ist gut.

Versehntliche Offenlegung ist keine Nachvollziehbarkeit.

Sie ist nur ein Sicherheitsvorfall mit Dokumentarhut.

## Repository-Status

Dieses Dokument leitet zukünftige Veröffentlichungsentscheidungen im Flextrawurst-Repository.

Siehe auch:

* `NOTICE.md`
* `SECURITY.md`
* `.gitignore`
