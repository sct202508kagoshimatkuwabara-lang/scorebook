# # apps/games/signals.py
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from apps.games.models import Lineup, Game

# @receiver(post_save, sender=Lineup)
# def update_lineup_json(sender, instance, **kwargs):
#     game = instance.game
#     # build_lineup_json をメソッド化したので必ず呼び出す
#     game.lineup_json = game.build_lineup_json()
#     game.save(update_fields=["lineup_json"])
