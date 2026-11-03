# Projet augmenté par l'IA

[![Vérifications contre reader-ergonomics](https://github.com/Tewf/ai-augmented-project/actions/workflows/checks.yml/badge.svg)](https://github.com/Tewf/ai-augmented-project/actions/workflows/checks.yml)
[![Site](https://github.com/Tewf/ai-augmented-project/actions/workflows/pages.yml/badge.svg)](https://tewf.github.io/ai-augmented-project/)

Comment une **personne**, un **modèle de langue** et une **machine** sont mis en place et mènent un projet ensemble. La
machine vérifie, le modèle reçoit ses consignes et ses limites, et la personne garde les décisions qui sont les
siennes ; une boucle joint les trois. Les étapes du projet sont celles de [reader-ergonomics-project](https://github.com/Tewf/reader-ergonomics-project) ;
ce dépôt ajoute les deux parties qui ne sont pas la personne, et la mise en place de chacune.

Cette page en anglais : [README.md](README.md). Les deux versions suivent le même état.

> **État (2026-11-03) :** le premier travail, une revue de littérature en première passe de 39 sources, est écrit et
> finit sur une référence nommée. Le document de conception est écrit et proposé ; il attend l'approbation du mainteneur. Le nom est gardé ; le mot du domaine
> est human-AI teaming. Ce n'est ni une norme officielle, ni une étude relue par des pairs, ni un résultat nouveau.
>
> **Comment il est fait :** avec Claude, un assistant IA d'Anthropic, sous la direction du mainteneur, comme
> reader-ergonomics. Les corrections sont bienvenues sous forme d'issues.

## Où il se place

![L'IDE met en œuvre et les agents utilisent ai-augmented-project, qui utilise reader-ergonomics-project pour les étapes et reader-ergonomics-blueprint pour le raisonnement vérifié ; les deux obéissent à la norme et au topic.](where-it-sits.svg)

<details>
<summary>Graphviz source</summary>

```dot
// Where ai-augmented-project sits. Colours: reader-ergonomics family blue, AI-augmented family green, the bridge
// orange, each named in its box; this repository has the thick border.
digraph where_it_sits {
  graph [rankdir=TB, nodesep=0.45, ranksep=0.5, bgcolor="white", pad=0.2, fontname="Inter"];
  node  [shape=box, style="rounded,filled", fontname="Inter", fontsize=13, margin="0.2,0.1", penwidth=1.5, fontcolor="#1F2328"];
  edge  [fontname="Inter", fontsize=11, color="#3D434B", fontcolor="#55575F", penwidth=1.3, arrowsize=0.8];
  IDE [label=<<b>ai-augmented-ide</b><br/><font point-size="11" color="#55575F">AI-augmented family: the tool</font>>, fillcolor="#E6F2EA", color="#2E7D4F"];
  AG  [label=<<b>ai-augmented-agents</b><br/><font point-size="11" color="#55575F">AI-augmented family: several agents</font>>, fillcolor="#E6F2EA", color="#2E7D4F"];
  AP  [label=<<b>ai-augmented-project</b><br/><font point-size="11" color="#55575F">AI-augmented family: one person, one model,</font><br/><font point-size="11" color="#55575F">one machine, one project</font>>, fillcolor="#E6F2EA", color="#2E7D4F", penwidth=2.6];
  P   [label=<<b>reader-ergonomics-project</b><br/><font point-size="11" color="#55575F">reader-ergonomics family: the steps</font>>, fillcolor="#E8EEF8", color="#2F5DA8"];
  BP  [label=<<b>reader-ergonomics-blueprint</b><br/><font point-size="11" color="#55575F">the bridge: reasoning checked,</font><br/><font point-size="11" color="#55575F">a model that guides</font>>, fillcolor="#FBEDE4", color="#B4541A"];
  RE  [label=<<b>reader-ergonomics, reader-ergonomics-topic</b><br/><font point-size="11" color="#55575F">the standard and the unit of writing</font>>, fillcolor="#E8EEF8", color="#2F5DA8"];
  IDE -> AP [label=" implements"];
  AG -> AP [label=" uses"];
  AP -> P [label=" uses"];
  AP -> BP [label=" uses"];
  P -> RE [label=" obeys"];
  BP -> RE [label=" obeys"];
}
```

</details>

- **Il utilise [reader-ergonomics-project](https://github.com/Tewf/reader-ergonomics-project)** pour les étapes d'un
  projet, et **[reader-ergonomics-blueprint](https://github.com/Tewf/reader-ergonomics-blueprint/blob/f9b2408e7f1ddf4a82d2d480c62d6b5855e14e0b/README.md)** pour la boucle où un
  modèle interprète le verdict d'un vérificateur et ne décide rien. Le blueprint est épinglé par commit, faute de version
  publiée.
- **Il obéit à [reader-ergonomics](https://github.com/Tewf/reader-ergonomics/blob/b9732b9814c71768f722691f3c5049ec2b8ed378/standard.md)** (v1.19.2) et exécute ses vérifications en CI.
- **Il ne pointe que vers le bas.** La carte de la famille est [ai-augmented](https://github.com/Tewf/ai-augmented).

## Périmètre

| | Quoi | Pourquoi |
|---|---|---|
| dedans | mettre en place la machine : environnements, hooks, vérifications et CI comme oracle de ce qu'un programme peut décider | ce qu'un programme peut vérifier, un programme le vérifie, avant qu'un modèle ne le lise |
| dedans | mettre en place le modèle : ses consignes permanentes, sa mémoire entre sessions, ce qu'on lui remet au départ, ce qu'il peut décider | une question posée deux fois, ou une décision prise par le modèle, est le coût que ce dépôt existe pour réduire |
| dedans | mettre en place la personne : comment elle lit, quelles décisions sont les siennes, comment une question lui parvient, avec des options | le temps de la personne est la ressource rare |
| dedans | la boucle : qui fait quoi à chaque étape du projet, et ce qui est mesuré pour dire que le dispositif marche | sans mesure, un dispositif est une habitude |
| dehors | les étapes du projet elles-mêmes | [reader-ergonomics-project](https://github.com/Tewf/reader-ergonomics-project) |
| dehors | la vérification du raisonnement lui-même, Lean d'abord | [reader-ergonomics-blueprint](https://github.com/Tewf/reader-ergonomics-blueprint) |
| dehors | plusieurs modèles ou plusieurs personnes sur un projet | [ai-augmented-agents](https://github.com/Tewf/ai-augmented-agents) |
| dehors | le logiciel | [ai-augmented-ide](https://github.com/Tewf/ai-augmented-ide) |
| dehors | construire ou entraîner un modèle | d'autres le font ; ce dépôt en utilise un |

## Le premier travail : une revue de littérature

Une première passe de 39 sources, 30 formelles et 9 grises, en cinq étapes comme une revue de thèse :
[cadre](evidence/human-ai-teaming/frame.md), [revue](evidence/human-ai-teaming/review.md),
[état de l'art](evidence/human-ai-teaming/state-of-the-art.md), [positionnement](evidence/human-ai-teaming/position.md)
et [référence](evidence/human-ai-teaming/baseline.md). Le dossier [evidence](evidence/) contient tout (en anglais).

## Ce que la revue a trouvé

- **Le nom du domaine est human-AI teaming.** Le but est l'intelligence hybride ; le test est la performance
  complémentaire. « AI-augmented » rappelle l'augmentation : le nom est proche et il est gardé.
- **Une personne avec un modèle ne bat pas en moyenne le meilleur des deux** : g = -0,23 sur 106 expériences.
  Les tâches qui décident perdent ; celles qui créent gagnent (Vaccaro 2024). Mesuré.
- **Un fichier de contexte n'améliore pas le succès et coûte plus de 20 % de plus en moyenne** ; il aide à énoncer une pratique
  hors norme (Gloaguen 2026). Un fichier périmé est suivi plutôt que le code dans 90,1 % des choix (Xu 2026,
  secondaire). Mesuré.
- **Les résultats sur la vitesse divergent.** Des développeurs expérimentés étaient 19 % plus lents.
  Ils se croyaient plus rapides (Becker 2025). Deux autres essais trouvent environ 21 % et 55,8 % plus rapides
  (secondaire). L'auto-évaluation n'est pas une mesure.
- **Aucune étude contrôlée n'a été trouvée** d'une mémoire de projet écrite par un modèle, de son audit, ni des
  allers-retours comme mesure. C'est un énoncé sur ces recherches.

## La référence

**B1** est la pratique du mainteneur, écrite pour cette revue ([référence](evidence/human-ai-teaming/baseline.md)).

- consignes permanentes chargées à chaque session ;
- une mémoire partagée, avec un fait par fichier ;
- les vérifications comme oracle ;
- la délégation selon le coût ;
- des questions à la personne, avec des options.

Il lui manque une mesure, un test de péremption et un témoin.
Le [positionnement](evidence/human-ai-teaming/position.md) a laissé quatre points au document :
l'unité de mesure et le témoin, où sont consignées les décisions de la personne, quelles vérifications sont des
programmes, comment un programme trouve les consignes périmées. Le document les tranche.

## Le document de conception

[design/one-project.md](design/one-project.md) est proposé le 2026-11-03, avec une fiche par choix.

- **Les décisions** ([0003](decisions/0003-the-model-decides-nothing-unchecked.md)) : la personne décide de ce qui
  est construit et des vérifications qui comptent, la machine tranche réussite ou échec, le modèle ne décide rien sans
  vérification.
- **Le début d'une session** ([0004](decisions/0004-a-short-start-file-and-an-index.md)) : un fichier de départ et un
  index de la mémoire, de 200 lignes au plus chacun (provisoire), et le brief de la tâche, et rien d'autre.
- **Le brief** ([0008](decisions/0008-a-task-is-handed-over-as-a-brief-that-names-its-checks.md)) : quatre parties, la
  tâche, ce qui est décidé, ce qu'il faut trouver et les vérifications qui le jugeront.
- **La mémoire** ([0005](decisions/0005-memory-is-plain-files-with-a-source.md)) : un fait par fichier, chacun avec
  une source qu'un programme suit ; une phrase donne la priorité au code sur un fichier périmé.
- **La mesure** ([0006](decisions/0006-the-task-is-the-unit-and-three-arms-the-control.md)) : cinq comptes par
  tâche, et un cas compare la personne seule, le modèle seul et les deux.
- **L'extension d'éditeur** ([0007](decisions/0007-the-extension-reads-files-and-hands-over-two.md)) : elle ne garde
  aucun état, montre les fichiers et remet au modèle le fichier de départ et l'index.

## Questions auxquelles la revue a répondu

Les réponses sont dans [positionnement](evidence/human-ai-teaming/position.md).

- **Décisions.** Quelles décisions reviennent à la personne, lesquelles à la machine, et que reste-t-il qu'un modèle
  puisse prendre ? La réponse du blueprint pour le raisonnement est : aucune ; vaut-elle pour tout un projet ?
- **Le début d'une session.** Que faut-il remettre à un modèle pour qu'aucune question ne soit posée deux fois, et
  comment garder cela assez court pour être lu ?
- **Mémoire.** Comment ce qu'un modèle retient entre sessions est-il conservé, qui peut l'écrire, et comment est-il audité ?
- **La mesure.** Que compte-t-on pour dire qu'un dispositif marche : allers-retours, temps, erreurs attrapées par une
  vérification avant qu'une personne ne les voie ?

## Vérifier

```sh
git clone https://github.com/Tewf/reader-ergonomics
python3 reader-ergonomics/checks/run.py chemin/vers/ce/depot
```

La CI exécute les mêmes vérifications à chaque push, et une exécution échoue à la première erreur
([checks.yml](https://github.com/Tewf/ai-augmented-project/blob/master/.github/workflows/checks.yml)). Chaque push sur
master construit aussi le site, [tewf.github.io/ai-augmented-project](https://tewf.github.io/ai-augmented-project/)
([pages.yml](https://github.com/Tewf/ai-augmented-project/blob/master/.github/workflows/pages.yml)).

## Contenu

| Partie | Résumé |
|---|---|
| [evidence](evidence/) | la revue de première passe : 39 sources, cinq étapes, finissant sur la référence B1 |
| [design](design/one-project.md) | le document de conception : cinq décisions, leurs solutions écartées, la mesure et l'interface de l'extension |
| [decisions](decisions/) | une fiche par choix qui façonne ce dépôt, chacune ouvrant sur la décision en une phrase |

## Licence

Code sous [Apache License 2.0](LICENSE) ; prose sous [CC BY 4.0](LICENSES/CC-BY-4.0.txt). Réutilisez-le comme vous le
souhaitez, en créditant ce dépôt ; [CITATION.cff](CITATION.cff) donne une citation si besoin.
