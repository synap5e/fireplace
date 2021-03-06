from hearthstone.enums import CardType, GameTag, Rarity

import utils


CARDS = utils.fireplace.cards.db


def test_all_tags_known():
	"""
	Iterate through the card database and check that all specified GameTags
	are known in hearthstone.enums.GameTag
	"""
	unknown_tags = set()
	known_tags = list(GameTag)
	known_rarities = list(Rarity)

	# Check the db loaded correctly
	assert utils.fireplace.cards.db

	for card in CARDS.values():
		card_tags = [int(e.attrib["enumID"]) for e in card.xml.findall("./Tag")]
		for tag in card_tags:
			# We have fake tags in fireplace.enums which are always negative
			if tag not in known_tags and tag > 0:
				unknown_tags.add(tag)

		# Test rarities as well (cf. TB_BlingBrawl_Blade1e in 10956...)
		assert card.rarity in known_rarities

	assert not unknown_tags


def test_play_scripts():
	for card in CARDS.values():
		if card.scripts.activate:
			assert card.type == CardType.HERO_POWER
		elif card.scripts.play:
			assert card.type not in (CardType.HERO, CardType.HERO_POWER, CardType.ENCHANTMENT)
