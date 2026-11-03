# bowling · Heliod Harness · every model call

**Passed** · 31/31 test cases · $0.0094 billed · 1 min · 12 model calls · input 284,235 tokens (246,330 cached) · output 4,475 tokens

[Attempt summary](README.md) · [diff](diff.patch) · [grade](grade.json) · [raw calls](calls.jsonl.gz)

Each call shows only what is new in the request (the rest is the conversation so far) and the full reply. Heliod's system prompts and tool definitions are removed; see METHODOLOGY.md.

## Call 1 · main agent

2,502 in (0 cached) · 72 out · $0.0003 · 1521 ms · OpenRouter id `gen-1793672206-I3hJE5lD6GjEsVcUFa8X`

**Request:**

**user**

```
Do the task described in TASK.md in this repository.
```

**Reply:**

→ tool `bash`

```
{
 "command": "ls -la && git ls-files",
 "timeout": 10000
}
```

→ tool `read`

```
{
 "path": "TASK.md"
}
```

## Call 2 · main agent

2,897 in (2,499 cached) · 86 out · $0.0001 · 1509 ms · OpenRouter id `gen-1793672207-VcCJOqbcksGESHPKX5qN`

**New in this request** (continues call 1):

**assistant → tool `bash`**

```
{
 "command": "ls -la && git ls-files",
 "timeout": 10000
}
```

**assistant → tool `read`**

```
{
 "path": "TASK.md"
}
```

**tool result** (`call_Af4IwzzRMSieuU77n3LHJR8M`)

```
total 40
drwxr-xr-x@  7 avneh  staff   224 Nov  2 18:16 .
drwxr-xr-x@  4 avneh  staff   128 Nov  2 18:16 ..
drwxr-xr-x@  4 avneh  staff   128 Nov  2 17:28 .docs
drwxr-xr-x@ 12 avneh  staff   384 Nov  2 18:16 .git
-rw-r--r--@  1 avneh  staff  8558 Nov  2 17:28 bowling_test.py
-rw-r--r--@  1 avneh  staff   131 Nov  2 17:28 bowling.py
-rw-r--r--@  1 avneh  staff   394 Nov  2 18:16 TASK.md
.docs/instructions.append.md
.docs/instructions.md
TASK.md
bowling.py
bowling_test.py

```

**tool result** (`call_cWoTv4Gw30rqBlOFBdkOlWdC`)

```
Solve the Exercism exercise in this directory.

Read the instructions in .docs/instructions.md and .docs/instructions.append.md. Implement the solution in bowling.py, keeping the existing function and class names, since the unit tests in bowling_test.py call them. Use only the standard library. Do not modify the test files.

Run the tests with: python3 -m pytest -q
Stop when all tests pass.

```

**Reply:**

→ tool `read`

```
{
 "path": ".docs/instructions.md"
}
```

→ tool `read`

```
{
 "path": ".docs/instructions.append.md"
}
```

→ tool `read`

```
{
 "path": "bowling.py"
}
```

→ tool `read`

```
{
 "path": "bowling_test.py"
}
```

## Call 3 · main agent

7,022 in (2,894 cached) · 1,418 out · $0.0013 · 12616 ms · OpenRouter id `gen-1793672209-lJYQ41ojfJK6Xq1Z6iWC`

**New in this request** (continues call 2):

**assistant → tool `read`**

```
{
 "path": ".docs/instructions.md"
}
```

**assistant → tool `read`**

```
{
 "path": ".docs/instructions.append.md"
}
```

**assistant → tool `read`**

```
{
 "path": "bowling.py"
}
```

**assistant → tool `read`**

```
{
 "path": "bowling_test.py"
}
```

**tool result** (`call_NiKxV4o8ilk9o3atERaf8fo6`)

<details><summary>57 lines</summary>

```
# Instructions

Score a bowling game.

Bowling is a game where players roll a heavy ball to knock down pins arranged in a triangle.
Write code to keep track of the score of a game of bowling.

## Scoring Bowling

The game consists of 10 frames.
A frame is composed of one or two ball throws with 10 pins standing at frame initialization.
There are three cases for the tabulation of a frame.

- An open frame is where a score of less than 10 is recorded for the frame.
  In this case the score for the frame is the number of pins knocked down.

- A spare is where all ten pins are knocked down by the second throw.
  The total value of a spare is 10 plus the number of pins knocked down in their next throw.

- A strike is where all ten pins are knocked down by the first throw.
  The total value of a strike is 10 plus the number of pins knocked down in the next two throws.
  If a strike is immediately followed by a second strike, then the value of the first strike cannot be determined until the ball is thrown one more time.

Here is a three frame example:

|  Frame 1   |  Frame 2   |     Frame 3      |
| :--------: | :--------: | :--------------: |
| X (strike) | 5/ (spare) | 9 0 (open frame) |

Frame 1 is (10 + 5 + 5) = 20

Frame 2 is (5 + 5 + 9) = 19

Frame 3 is (9 + 0) = 9

This means the current running total is 48.

The tenth frame in the game is a special case.
If someone throws a spare or a strike then they get one or two fill balls respectively.
Fill balls exist to calculate the total of the 10th frame.
Scoring a strike or spare on the fill ball does not give the player more fill balls.
The total value of the 10th frame is the total number of pins knocked down.

For a tenth frame of X1/ (strike and a spare), the total value is 20.

For a tenth frame of XXX (three strikes), the total value is 30.

## Requirements

Write code to keep track of the score of a game of bowling.
It should support two operations:

- `roll(pins : int)` is called each time the player rolls a ball.
  The argument is the number of pins knocked down.
- `score() : int` is called only at the very end of the game.
  It returns the total score for that game.

```

</details>

**tool result** (`call_k8xy7xW8uwB29YmjTTWebTQA`)

````
# Instructions append

## Exception messages

Sometimes it is necessary to [raise an exception](https://docs.python.org/3/tutorial/errors.html#raising-exceptions). When you do this, you should always include a **meaningful error message** to indicate what the source of the error is. This makes your code more readable and helps significantly with debugging. For situations where you know that the error source will be a certain type, you can choose to raise one of the [built in error types](https://docs.python.org/3/library/exceptions.html#base-classes), but should still include a meaningful message.

This particular exercise requires that you use the [raise statement](https://docs.python.org/3/reference/simple_stmts.html#the-raise-statement) to "throw" an error when the scoring or playing rules are not followed. The tests will only pass if you both `raise` the `exception` and include a message with it.

To raise a `ValueError` with a message, write the message as an argument to the `exception` type:

```python
# example when a bonus is attempted with an open frame
raise IndexError("cannot throw bonus with an open tenth frame")

# example when fill balls are invalid
raise ValueError("invalid fill balls")
```

````

**tool result** (`call_P7bQ2BepBYPKk29CUlDqoPvP`)

```
class BowlingGame:
    def __init__(self):
        pass

    def roll(self, pins):
        pass

    def score(self):
        pass

```

**tool result** (`call_FIrqNZmV9KcLliUfdpLJJCwK`)

<details><summary>214 lines</summary>

```
# These tests are auto-generated with test data from:
# https://github.com/exercism/problem-specifications/tree/main/exercises/bowling/canonical-data.json
# File last updated on 2023-07-21

import unittest

from bowling import (
    BowlingGame,
)


class BowlingTest(unittest.TestCase):
    def roll_new_game(self, rolls):
        game = BowlingGame()
        for roll in rolls:
            game.roll(roll)
        return game

    def test_should_be_able_to_score_a_game_with_all_zeros(self):
        rolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        game = self.roll_new_game(rolls)
        self.assertEqual(game.score(), 0)

    def test_should_be_able_to_score_a_game_with_no_strikes_or_spares(self):
        rolls = [3, 6, 3, 6, 3, 6, 3, 6, 3, 6, 3, 6, 3, 6, 3, 6, 3, 6, 3, 6]
        game = self.roll_new_game(rolls)
        self.assertEqual(game.score(), 90)

    def test_a_spare_followed_by_zeros_is_worth_ten_points(self):
        rolls = [6, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        game = self.roll_new_game(rolls)
        self.assertEqual(game.score(), 10)

    def test_points_scored_in_the_roll_after_a_spare_are_counted_twice(self):
        rolls = [6, 4, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        game = self.roll_new_game(rolls)
        self.assertEqual(game.score(), 16)

    def test_consecutive_spares_each_get_a_one_roll_bonus(self):
        rolls = [5, 5, 3, 7, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        game = self.roll_new_game(rolls)
        self.assertEqual(game.score(), 31)

    def test_a_spare_in_the_last_frame_gets_a_one_roll_bonus_that_is_counted_once(self):
        rolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 3, 7]
        game = self.roll_new_game(rolls)
        self.assertEqual(game.score(), 17)

    def test_a_strike_earns_ten_points_in_a_frame_with_a_single_roll(self):
        rolls = [10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        game = self.roll_new_game(rolls)
        self.assertEqual(game.score(), 10)

    def test_points_scored_in_the_two_rolls_after_a_strike_are_counted_twice_as_a_bonus(
        self,
    ):
        rolls = [10, 5, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        game = self.roll_new_game(rolls)
        self.assertEqual(game.score(), 26)

    def test_consecutive_strikes_each_get_the_two_roll_bonus(self):
        rolls = [10, 10, 10, 5, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        game = self.roll_new_game(rolls)
        self.assertEqual(game.score(), 81)

    def test_a_strike_in_the_last_frame_gets_a_two_roll_bonus_that_is_counted_once(
        self,
    ):
        rolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 7, 1]
        game = self.roll_new_game(rolls)
        self.assertEqual(game.score(), 18)

    def test_rolling_a_spare_with_the_two_roll_bonus_does_not_get_a_bonus_roll(self):
        rolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 7, 3]
        game = self.roll_new_game(rolls)
        self.assertEqual(game.score(), 20)

    def test_strikes_with_the_two_roll_bonus_do_not_get_bonus_rolls(self):
        rolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 10, 10]
        game = self.roll_new_game(rolls)
        self.assertEqual(game.score(), 30)

    def test_last_two_strikes_followed_by_only_last_bonus_with_non_strike_points(self):
        rolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 10, 0, 1]
        game = self.roll_new_game(rolls)
        self.assertEqual(game.score(), 31)

    def test_a_strike_with_the_one_roll_bonus_after_a_spare_in_the_last_frame_does_not_get_a_bonus(
        self,
    ):
        rolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 3, 10]
        game = self.roll_new_game(rolls)
        self.assertEqual(game.score(), 20)

    def test_all_strikes_is_a_perfect_game(self):
        rolls = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
        game = self.roll_new_game(rolls)
        self.assertEqual(game.score(), 300)

    def test_rolls_cannot_score_negative_points(self):
        rolls = []
        game = self.roll_new_game(rolls)
        with self.assertRaisesWithMessage(Exception):
            game.roll(-1)

    def test_a_roll_cannot_score_more_than_10_points(self):
        rolls = []
        game = self.roll_new_game(rolls)
        with self.assertRaisesWithMessage(Exception):
            game.roll(11)

    def test_two_rolls_in_a_frame_cannot_score_more_than_10_points(self):
        rolls = [5]
        game = self.roll_new_game(rolls)
        with self.assertRaisesWithMessage(Exception):
            game.roll(6)

    def test_bonus_roll_after_a_strike_in_the_last_frame_cannot_score_more_than_10_points(
        self,
    ):
        rolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10]
        game = self.roll_new_game(rolls)
        with self.assertRaisesWithMessage(Exception):
            game.roll(11)

    def test_two_bonus_rolls_after_a_strike_in_the_last_frame_cannot_score_more_than_10_points(
        self,
    ):
        rolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 5]
        game = self.roll_new_game(rolls)
        with self.assertRaisesWithMessage(Exception):
            game.roll(6)

    def test_two_bonus_rolls_after_a_strike_in_the_last_frame_can_score_more_than_10_points_if_one_is_a_strike(
        self,
    ):
        rolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 10, 6]
        game = self.roll_new_game(rolls)
        self.assertEqual(game.score(), 26)

    def test_the_second_bonus_rolls_after_a_strike_in_the_last_frame_cannot_be_a_strike_if_the_first_one_is_not_a_strike(
        self,
    ):
        rolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 6]
        game = self.roll_new_game(rolls)
        with self.assertRaisesWithMessage(Exception):
            game.roll(10)

    def test_second_bonus_roll_after_a_strike_in_the_last_frame_cannot_score_more_than_10_points(
        self,
    ):
        rolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 10]
        game = self.roll_new_game(rolls)
        with self.assertRaisesWithMessage(Exception):
            game.roll(11)

    def test_an_unstarted_game_cannot_be_scored(self):
        rolls = []
        game = self.roll_new_game(rolls)
        with self.assertRaisesWithMessage(Exception):
            game.score()

    def test_an_incomplete_game_cannot_be_scored(self):
        rolls = [0, 0]
        game = self.roll_new_game(rolls)
        with self.assertRaisesWithMessage(Exception):
            game.score()

    def test_cannot_roll_if_game_already_has_ten_frames(self):
        rolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        game = self.roll_new_game(rolls)
        with self.assertRaisesWithMessage(Exception):
            game.roll(0)

    def test_bonus_rolls_for_a_strike_in_the_last_frame_must_be_rolled_before_score_can_be_calculated(
        self,
    ):
        rolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10]
        game = self.roll_new_game(rolls)
        with self.assertRaisesWithMessage(Exception):
            game.score()

    def test_both_bonus_rolls_for_a_strike_in_the_last_frame_must_be_rolled_before_score_can_be_calculated(
        self,
    ):
        rolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 10]
        game = self.roll_new_game(rolls)
        with self.assertRaisesWithMessage(Exception):
            game.score()

    def test_bonus_roll_for_a_spare_in_the_last_frame_must_be_rolled_before_score_can_be_calculated(
        self,
    ):
        rolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 3]
        game = self.roll_new_game(rolls)
        with self.assertRaisesWithMessage(Exception):
            game.score()

    def test_cannot_roll_after_bonus_roll_for_spare(self):
        rolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 3, 2]
        game = self.roll_new_game(rolls)
        with self.assertRaisesWithMessage(Exception):
            game.roll(2)

    def test_cannot_roll_after_bonus_rolls_for_strike(self):
        rolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 3, 2]
        game = self.roll_new_game(rolls)
        with self.assertRaisesWithMessage(Exception):
            game.roll(2)

    # Utility functions
    def assertRaisesWithMessage(self, exception):
        return self.assertRaisesRegex(exception, r".+")

```

</details>

**Reply:**

*reasoning:* **Validating frame rolls state**

I'm implementing a validation for the rolls based on frames and their history. For frames less than 10, I’ll process them sequentially. To prevent issues, I need to ensure there aren’t more than 10 rolls if the first two aren’t strikes. The 10th frame requires special validation. I can track each roll index and calculate completed frames over the first nine rolls—valid sequences included. I’ll need to ensure the total rolls are within bounds too.**Handling frame rolls and scoring**

I’m examining how to handle the ValueError in the range of less than 0 or greater than 10 for cumulative frames. For the tenth frame, after completing nine, I’ll check the roll history. If the roll is zero, it’s valid. If it’s one, I check conditions for a spare and strikes. The calculations for subsequent rolls depend on previous outcomes. I’ll use a frame cursor to parse through the rolls and validate scores based on the complete count and frame conditions.**Calculating roll scores**

I need to ensure that during the roll call, if the current index exceeds the length, I manage the frame completion count carefully. I’ll score the first nine frames in a loop, then sum the remaining rolls. If there’s an insufficiency, I should raise an error. For the initial nine frames, I need to check that the index is available. It’s important to validate that the total number of rolls is sufficient before scoring, following the established rules.**Clarifying rolls conditions**

I'm finalizing the rolls list. For the tenth condition, I need to ensure that a strike requires three rolls, a spare also needs three, and an open frame should have two rolls. I must be careful since no impossible overrolls are allowed. Let's get that down clearly!

→ tool `write`

```
{
 "path": "bowling.py",
 "content": "class BowlingGame:\n    def __init__(self):\n        self.rolls = []\n\n    def _first_nine_end(self):\n        \"\"\"Return the roll index at which the tenth frame begins.\"\"\"\n        index = 0\n        for _ in range(9):\n            if index >= len(self.rolls):\n                return None\n            if self.rolls[index] == 10:\n                index += 1\n            else:\n                if index + 1 >= len(self.rolls):\n                    return None\n                index += 2\n        return index\n\n    def roll(self, pins):\n        if not isinstance(pins, int) or pins < 0 or pins > 10:\n            raise ValueError(\"pins must be an integer between 0 and 10\")\n\n        tenth_start = self._first_nine_end()\n        if tenth_start is None:\n            # A frame among the first nine is in progress.\n            if self.rolls and self.rolls[-1] != 10:\n                frame_start = len(self.rolls) - 1\n                # Locate the start of the current frame by parsing completed frames.\n                index = 0\n                while index < frame_start:\n                    index += 1 if self.rolls[index] == 10 else 2\n                if self.rolls[index] + pins > 10:\n                    raise ValueError(\"a frame cannot knock down more than 10 pins\")\n        else:\n            frame_rolls = self.rolls[tenth_start:]\n            if len(frame_rolls) == 0:\n                pass\n            elif len(frame_rolls) == 1:\n                if frame_rolls[0] != 10 and frame_rolls[0] + pins > 10:\n                    raise ValueError(\"a frame cannot knock down more than 10 pins\")\n            elif len(frame_rolls) == 2:\n                first, second = frame_rolls\n                if first == 10:\n                    if second != 10 and second + pins > 10:\n                        raise ValueError(\"fill balls cannot knock down more than 10 pins\")\n                elif first + second == 10:\n                    pass  # Spare fill ball: a fresh rack is available.\n                else:\n                    raise ValueError(\"cannot roll after an open tenth frame\")\n            else:\n                raise ValueError(\"the game is already complete\")\n        self.rolls.append(pins)\n\n    def score(self):\n        tenth_start = self._first_nine_end()\n        if tenth_start is None:\n            raise ValueError(\"cannot score an incomplete game\")\n\n        tenth = self.rolls[tenth_start:]\n        if not tenth:\n            raise ValueError(\"cannot score an incomplete game\")\n        if tenth[0] == 10:\n            if len(tenth) != 3:\n                raise ValueError(\"strike fill balls are incomplete\")\n        elif len(tenth) == 2 and sum(tenth) == 10:\n            raise ValueError(\"spare fill ball is missing\")\n        elif len(tenth) != 2:\n            raise ValueError(\"cannot score an incomplete game\")\n\n        total = sum(tenth)\n        index = 0\n        for _ in range(9):\n            if self.rolls[index] == 10:\n                total += 10 + self.rolls[index + 1] + self.rolls[index + 2]\n                index += 1\n            else:\n                frame_total = self.rolls[index] + self.rolls[index + 1]\n                total += frame_total\n                if frame_total == 10:\n                    total += self.rolls[index + 2]\n                index += 2\n        return total\n"
}
```

## Call 4 · main agent

8,459 in (7,019 cached) · 292 out · $0.0004 · 5299 ms · OpenRouter id `gen-1793672221-rmwjTmp5yjaXtx9lufLu`

**New in this request** (continues call 3):

**assistant → tool `write`**

```
{
 "path": "bowling.py",
 "content": "class BowlingGame:\n    def __init__(self):\n        self.rolls = []\n\n    def _first_nine_end(self):\n        \"\"\"Return the roll index at which the tenth frame begins.\"\"\"\n        index = 0\n        for _ in range(9):\n            if index >= len(self.rolls):\n                return None\n            if self.rolls[index] == 10:\n                index += 1\n            else:\n                if index + 1 >= len(self.rolls):\n                    return None\n                index += 2\n        return index\n\n    def roll(self, pins):\n        if not isinstance(pins, int) or pins < 0 or pins > 10:\n            raise ValueError(\"pins must be an integer between 0 and 10\")\n\n        tenth_start = self._first_nine_end()\n        if tenth_start is None:\n            # A frame among the first nine is in progress.\n            if self.rolls and self.rolls[-1] != 10:\n                frame_start = len(self.rolls) - 1\n                # Locate the start of the current frame by parsing completed frames.\n                index = 0\n                while index < frame_start:\n                    index += 1 if self.rolls[index] == 10 else 2\n                if self.rolls[index] + pins > 10:\n                    raise ValueError(\"a frame cannot knock down more than 10 pins\")\n        else:\n            frame_rolls = self.rolls[tenth_start:]\n            if len(frame_rolls) == 0:\n                pass\n            elif len(frame_rolls) == 1:\n                if frame_rolls[0] != 10 and frame_rolls[0] + pins > 10:\n                    raise ValueError(\"a frame cannot knock down more than 10 pins\")\n            elif len(frame_rolls) == 2:\n                first, second = frame_rolls\n                if first == 10:\n                    if second != 10 and second + pins > 10:\n                        raise ValueError(\"fill balls cannot knock down more than 10 pins\")\n                elif first + second == 10:\n                    pass  # Spare fill ball: a fresh rack is available.\n                else:\n                    raise ValueError(\"cannot roll after an open tenth frame\")\n            else:\n                raise ValueError(\"the game is already complete\")\n        self.rolls.append(pins)\n\n    def score(self):\n        tenth_start = self._first_nine_end()\n        if tenth_start is None:\n            raise ValueError(\"cannot score an incomplete game\")\n\n        tenth = self.rolls[tenth_start:]\n        if not tenth:\n            raise ValueError(\"cannot score an incomplete game\")\n        if tenth[0] == 10:\n            if len(tenth) != 3:\n                raise ValueError(\"strike fill balls are incomplete\")\n        elif len(tenth) == 2 and sum(tenth) == 10:\n            raise ValueError(\"spare fill ball is missing\")\n        elif len(tenth) != 2:\n            raise ValueError(\"cannot score an incomplete game\")\n\n        total = sum(tenth)\n        index = 0\n        for _ in range(9):\n            if self.rolls[index] == 10:\n                total += 10 + self.rolls[index + 1] + self.rolls[index + 2]\n                index += 1\n            else:\n                frame_total = self.rolls[index] + self.rolls[index + 1]\n                total += frame_total\n                if frame_total == 10:\n                    total += self.rolls[index + 2]\n                index += 2\n        return total\n"
}
```

**tool result** (`call_btrVK1456eRmjFD31XGxxqa8`)

```
Successfully wrote 3271 bytes to bowling.py
```

**Reply:**

*reasoning:* **Considering scoring rules**

I'm trying to figure out the rules for scoring in a bowling game, especially for the tenth frame. If the first nine frames aren't complete and the first roll is a 10, it looks like that might skip validation and be accepted as a strike. I wonder about the scoring logic for an open frame or if there are issues with overrolls being blocked. It seems like I need to test this logic to clarify.

→ tool `bash`

```
{
 "command": "python3 -m pytest -q",
 "timeout": 120000
}
```

## Call 5 · main agent

21,486 in (8,456 cached) · 395 out · $0.0019 · 4906 ms · OpenRouter id `gen-1793672227-vi5oDHDDjZ8VzGLD0cBX`

**New in this request** (continues call 4):

**assistant → tool `bash`**

```
{
 "command": "python3 -m pytest -q",
 "timeout": 120000
}
```

**tool result** (`call_tUuX8BkCklbUnK9w1SQhnLdj`)

<details><summary>929 lines</summary>

```
.FFFFF...FFFFFFFFFFFFF.FFFFFFF.                                          [100%]
=================================== FAILURES ===================================
________ BowlingTest.test_a_spare_followed_by_zeros_is_worth_ten_points ________

self = <bowling_test.BowlingTest testMethod=test_a_spare_followed_by_zeros_is_worth_ten_points>

    def test_a_spare_followed_by_zeros_is_worth_ten_points(self):
        rolls = [6, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
>       game = self.roll_new_game(rolls)
               ^^^^^^^^^^^^^^^^^^^^^^^^^

bowling_test.py:31: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
bowling_test.py:16: in roll_new_game
    game.roll(roll)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <bowling.BowlingGame object at 0x10747bc50>, pins = 0

    def roll(self, pins):
        if not isinstance(pins, int) or pins < 0 or pins > 10:
            raise ValueError("pins must be an integer between 0 and 10")
    
        tenth_start = self._first_nine_end()
        if tenth_start is None:
            # A frame among the first nine is in progress.
            if self.rolls and self.rolls[-1] != 10:
                frame_start = len(self.rolls) - 1
                # Locate the start of the current frame by parsing completed frames.
                index = 0
                while index < frame_start:
                    index += 1 if self.rolls[index] == 10 else 2
>               if self.rolls[index] + pins > 10:
                   ^^^^^^^^^^^^^^^^^
E               IndexError: list index out of range

bowling.py:32: IndexError
_ BowlingTest.test_a_spare_in_the_last_frame_gets_a_one_roll_bonus_that_is_counted_once _

self = <bowling_test.BowlingTest testMethod=test_a_spare_in_the_last_frame_gets_a_one_roll_bonus_that_is_counted_once>

    def test_a_spare_in_the_last_frame_gets_a_one_roll_bonus_that_is_counted_once(self):
        rolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 3, 7]
>       game = self.roll_new_game(rolls)
               ^^^^^^^^^^^^^^^^^^^^^^^^^

bowling_test.py:46: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
bowling_test.py:16: in roll_new_game
    game.roll(roll)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <bowling.BowlingGame object at 0x107b8bed0>, pins = 0

    def roll(self, pins):
        if not isinstance(pins, int) or pins < 0 or pins > 10:
            raise ValueError("pins must be an integer between 0 and 10")
    
        tenth_start = self._first_nine_end()
        if tenth_start is None:
            # A frame among the first nine is in progress.
            if self.rolls and self.rolls[-1] != 10:
                frame_start = len(self.rolls) - 1
                # Locate the start of the current frame by parsing completed frames.
                index = 0
                while index < frame_start:
                    index += 1 if self.rolls[index] == 10 else 2
>               if self.rolls[index] + pins > 10:
                   ^^^^^^^^^^^^^^^^^
E               IndexError: list index out of range

bowling.py:32: IndexError
___ BowlingTest.test_a_strike_earns_ten_points_in_a_frame_with_a_single_roll ___

self = <bowling_test.BowlingTest testMethod=test_a_strike_earns_ten_points_in_a_frame_with_a_single_roll>

    def test_a_strike_earns_ten_points_in_a_frame_with_a_single_roll(self):
        rolls = [10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
>       game = self.roll_new_game(rolls)
               ^^^^^^^^^^^^^^^^^^^^^^^^^

bowling_test.py:51: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
bowling_test.py:16: in roll_new_game
    game.roll(roll)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <bowling.BowlingGame object at 0x1074ba650>, pins = 0

    def roll(self, pins):
        if not isinstance(pins, int) or pins < 0 or pins > 10:
            raise ValueError("pins must be an integer between 0 and 10")
    
        tenth_start = self._first_nine_end()
        if tenth_start is None:
            # A frame among the first nine is in progress.
            if self.rolls and self.rolls[-1] != 10:
                frame_start = len(self.rolls) - 1
                # Locate the start of the current frame by parsing completed frames.
                index = 0
                while index < frame_start:
                    index += 1 if self.rolls[index] == 10 else 2
>               if self.rolls[index] + pins > 10:
                   ^^^^^^^^^^^^^^^^^
E               IndexError: list index out of range

bowling.py:32: IndexError
_ BowlingTest.test_a_strike_in_the_last_frame_gets_a_two_roll_bonus_that_is_counted_once _

self = <bowling_test.BowlingTest testMethod=test_a_strike_in_the_last_frame_gets_a_two_roll_bonus_that_is_counted_once>

    def test_a_strike_in_the_last_frame_gets_a_two_roll_bonus_that_is_counted_once(
        self,
    ):
        rolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 7, 1]
>       game = self.roll_new_game(rolls)
               ^^^^^^^^^^^^^^^^^^^^^^^^^

bowling_test.py:70: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
bowling_test.py:16: in roll_new_game
    game.roll(roll)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <bowling.BowlingGame object at 0x1074ba9e0>, pins = 0

    def roll(self, pins):
        if not isinstance(pins, int) or pins < 0 or pins > 10:
            raise ValueError("pins must be an integer between 0 and 10")
    
        tenth_start = self._first_nine_end()
        if tenth_start is None:
            # A frame among the first nine is in progress.
            if self.rolls and self.rolls[-1] != 10:
                frame_start = len(self.rolls) - 1
                # Locate the start of the current frame by parsing completed frames.
                index = 0
                while index < frame_start:
                    index += 1 if self.rolls[index] == 10 else 2
>               if self.rolls[index] + pins > 10:
                   ^^^^^^^^^^^^^^^^^
E               IndexError: list index out of range

bowling.py:32: IndexError
_ BowlingTest.test_a_strike_with_the_one_roll_bonus_after_a_spare_in_the_last_frame_does_not_get_a_bonus _

self = <bowling_test.BowlingTest testMethod=test_a_strike_with_the_one_roll_bonus_after_a_spare_in_the_last_frame_does_not_get_a_bonus>

    def test_a_strike_with_the_one_roll_bonus_after_a_spare_in_the_last_frame_does_not_get_a_bonus(
        self,
    ):
        rolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 3, 10]
>       game = self.roll_new_game(rolls)
               ^^^^^^^^^^^^^^^^^^^^^^^^^

bowling_test.py:92: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
bowling_test.py:16: in roll_new_game
    game.roll(roll)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <bowling.BowlingGame object at 0x107b94b90>, pins = 0

    def roll(self, pins):
        if not isinstance(pins, int) or pins < 0 or pins > 10:
            raise ValueError("pins must be an integer between 0 and 10")
    
        tenth_start = self._first_nine_end()
        if tenth_start is None:
            # A frame among the first nine is in progress.
            if self.rolls and self.rolls[-1] != 10:
                frame_start = len(self.rolls) - 1
                # Locate the start of the current frame by parsing completed frames.
                index = 0
                while index < frame_start:
                    index += 1 if self.rolls[index] == 10 else 2
>               if self.rolls[index] + pins > 10:
                   ^^^^^^^^^^^^^^^^^
E               IndexError: list index out of range

bowling.py:32: IndexError
_ BowlingTest.test_bonus_roll_after_a_strike_in_the_last_frame_cannot_score_more_than_10_points _

self = <bowling_test.BowlingTest testMethod=test_bonus_roll_after_a_strike_in_the_last_frame_cannot_score_more_than_10_points>

    def test_bonus_roll_after_a_strike_in_the_last_frame_cannot_score_more_than_10_points(
        self,
    ):
        rolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10]
>       game = self.roll_new_game(rolls)
               ^^^^^^^^^^^^^^^^^^^^^^^^^

bowling_test.py:122: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
bowling_test.py:16: in roll_new_game
    game.roll(roll)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <bowling.BowlingGame object at 0x107bb4250>, pins = 0

    def roll(self, pins):
        if not isinstance(pins, int) or pins < 0 or pins > 10:
            raise ValueError("pins must be an integer between 0 and 10")
    
        tenth_start = self._first_nine_end()
        if tenth_start is None:
            # A frame among the first nine is in progress.
            if self.rolls and self.rolls[-1] != 10:
                frame_start = len(self.rolls) - 1
                # Locate the start of the current frame by parsing completed frames.
                index = 0
                while index < frame_start:
                    index += 1 if self.rolls[index] == 10 else 2
>               if self.rolls[index] + pins > 10:
                   ^^^^^^^^^^^^^^^^^
E               IndexError: list index out of range

bowling.py:32: IndexError
_ BowlingTest.test_bonus_roll_for_a_spare_in_the_last_frame_must_be_rolled_before_score_can_be_calculated _

self = <bowling_test.BowlingTest testMethod=test_bonus_roll_for_a_spare_in_the_last_frame_must_be_rolled_before_score_can_be_calculated>

    def test_bonus_roll_for_a_spare_in_the_last_frame_must_be_rolled_before_score_can_be_calculated(
        self,
    ):
        rolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 3]
>       game = self.roll_new_game(rolls)
               ^^^^^^^^^^^^^^^^^^^^^^^^^

bowling_test.py:195: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
bowling_test.py:16: in roll_new_game
    game.roll(roll)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <bowling.BowlingGame object at 0x107bf9400>, pins = 0

    def roll(self, pins):
        if not isinstance(pins, int) or pins < 0 or pins > 10:
            raise ValueError("pins must be an integer between 0 and 10")
    
        tenth_start = self._first_nine_end()
        if tenth_start is None:
            # A frame among the first nine is in progress.
            if self.rolls and self.rolls[-1] != 10:
                frame_start = len(self.rolls) - 1
                # Locate the start of the current frame by parsing completed frames.
                index = 0
                while index < frame_start:
                    index += 1 if self.rolls[index] == 10 else 2
>               if self.rolls[index] + pins > 10:
                   ^^^^^^^^^^^^^^^^^
E               IndexError: list index out of range

bowling.py:32: IndexError
_ BowlingTest.test_bonus_rolls_for_a_strike_in_the_last_frame_must_be_rolled_before_score_can_be_calculated _

self = <bowling_test.BowlingTest testMethod=test_bonus_rolls_for_a_strike_in_the_last_frame_must_be_rolled_before_score_can_be_calculated>

    def test_bonus_rolls_for_a_strike_in_the_last_frame_must_be_rolled_before_score_can_be_calculated(
        self,
    ):
        rolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10]
>       game = self.roll_new_game(rolls)
               ^^^^^^^^^^^^^^^^^^^^^^^^^

bowling_test.py:179: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
bowling_test.py:16: in roll_new_game
    game.roll(roll)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <bowling.BowlingGame object at 0x10744f890>, pins = 0

    def roll(self, pins):
        if not isinstance(pins, int) or pins < 0 or pins > 10:
            raise ValueError("pins must be an integer between 0 and 10")
    
        tenth_start = self._first_nine_end()
        if tenth_start is None:
            # A frame among the first nine is in progress.
            if self.rolls and self.rolls[-1] != 10:
                frame_start = len(self.rolls) - 1
                # Locate the start of the current frame by parsing completed frames.
                index = 0
                while index < frame_start:
                    index += 1 if self.rolls[index] == 10 else 2
>               if self.rolls[index] + pins > 10:
                   ^^^^^^^^^^^^^^^^^
E               IndexError: list index out of range

bowling.py:32: IndexError
_ BowlingTest.test_both_bonus_rolls_for_a_strike_in_the_last_frame_must_be_rolled_before_score_can_be_calculated _

self = <bowling_test.BowlingTest testMethod=test_both_bonus_rolls_for_a_strike_in_the_last_frame_must_be_rolled_before_score_can_be_calculated>

    def test_both_bonus_rolls_for_a_strike_in_the_last_frame_must_be_rolled_before_score_can_be_calculated(
        self,
    ):
        rolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 10]
>       game = self.roll_new_game(rolls)
               ^^^^^^^^^^^^^^^^^^^^^^^^^

bowling_test.py:187: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
bowling_test.py:16: in roll_new_game
    game.roll(roll)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <bowling.BowlingGame object at 0x10752ac10>, pins = 0

    def roll(self, pins):
        if not isinstance(pins, int) or pins < 0 or pins > 10:
            raise ValueError("pins must be an integer between 0 and 10")
    
        tenth_start = self._first_nine_end()
        if tenth_start is None:
            # A frame among the first nine is in progress.
            if self.rolls and self.rolls[-1] != 10:
                frame_start = len(self.rolls) - 1
                # Locate the start of the current frame by parsing completed frames.
                index = 0
                while index < frame_start:
                    index += 1 if self.rolls[index] == 10 else 2
>               if self.rolls[index] + pins > 10:
                   ^^^^^^^^^^^^^^^^^
E               IndexError: list index out of range

bowling.py:32: IndexError
___________ BowlingTest.test_cannot_roll_after_bonus_roll_for_spare ____________

self = <bowling_test.BowlingTest testMethod=test_cannot_roll_after_bonus_roll_for_spare>

    def test_cannot_roll_after_bonus_roll_for_spare(self):
        rolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 3, 2]
>       game = self.roll_new_game(rolls)
               ^^^^^^^^^^^^^^^^^^^^^^^^^

bowling_test.py:201: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
bowling_test.py:16: in roll_new_game
    game.roll(roll)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <bowling.BowlingGame object at 0x107529b70>, pins = 0

    def roll(self, pins):
        if not isinstance(pins, int) or pins < 0 or pins > 10:
            raise ValueError("pins must be an integer between 0 and 10")
    
        tenth_start = self._first_nine_end()
        if tenth_start is None:
            # A frame among the first nine is in progress.
            if self.rolls and self.rolls[-1] != 10:
                frame_start = len(self.rolls) - 1
                # Locate the start of the current frame by parsing completed frames.
                index = 0
                while index < frame_start:
                    index += 1 if self.rolls[index] == 10 else 2
>               if self.rolls[index] + pins > 10:
                   ^^^^^^^^^^^^^^^^^
E               IndexError: list index out of range

bowling.py:32: IndexError
__________ BowlingTest.test_cannot_roll_after_bonus_rolls_for_strike ___________

self = <bowling_test.BowlingTest testMethod=test_cannot_roll_after_bonus_rolls_for_strike>

    def test_cannot_roll_after_bonus_rolls_for_strike(self):
        rolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 3, 2]
>       game = self.roll_new_game(rolls)
               ^^^^^^^^^^^^^^^^^^^^^^^^^

bowling_test.py:207: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
bowling_test.py:16: in roll_new_game
    game.roll(roll)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <bowling.BowlingGame object at 0x107b8c600>, pins = 0

    def roll(self, pins):
        if not isinstance(pins, int) or pins < 0 or pins > 10:
            raise ValueError("pins must be an integer between 0 and 10")
    
        tenth_start = self._first_nine_end()
        if tenth_start is None:
            # A frame among the first nine is in progress.
            if self.rolls and self.rolls[-1] != 10:
                frame_start = len(self.rolls) - 1
                # Locate the start of the current frame by parsing completed frames.
                index = 0
                while index < frame_start:
                    index += 1 if self.rolls[index] == 10 else 2
>               if self.rolls[index] + pins > 10:
                   ^^^^^^^^^^^^^^^^^
E               IndexError: list index out of range

bowling.py:32: IndexError
_________ BowlingTest.test_cannot_roll_if_game_already_has_ten_frames __________

self = <bowling_test.BowlingTest testMethod=test_cannot_roll_if_game_already_has_ten_frames>

    def test_cannot_roll_if_game_already_has_ten_frames(self):
        rolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
>       game = self.roll_new_game(rolls)
               ^^^^^^^^^^^^^^^^^^^^^^^^^

bowling_test.py:171: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
bowling_test.py:16: in roll_new_game
    game.roll(roll)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <bowling.BowlingGame object at 0x107b98650>, pins = 0

    def roll(self, pins):
        if not isinstance(pins, int) or pins < 0 or pins > 10:
            raise ValueError("pins must be an integer between 0 and 10")
    
        tenth_start = self._first_nine_end()
        if tenth_start is None:
            # A frame among the first nine is in progress.
            if self.rolls and self.rolls[-1] != 10:
                frame_start = len(self.rolls) - 1
                # Locate the start of the current frame by parsing completed frames.
                index = 0
                while index < frame_start:
                    index += 1 if self.rolls[index] == 10 else 2
>               if self.rolls[index] + pins > 10:
                   ^^^^^^^^^^^^^^^^^
E               IndexError: list index out of range

bowling.py:32: IndexError
________ BowlingTest.test_consecutive_spares_each_get_a_one_roll_bonus _________

self = <bowling_test.BowlingTest testMethod=test_consecutive_spares_each_get_a_one_roll_bonus>

    def test_consecutive_spares_each_get_a_one_roll_bonus(self):
        rolls = [5, 5, 3, 7, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
>       game = self.roll_new_game(rolls)
               ^^^^^^^^^^^^^^^^^^^^^^^^^

bowling_test.py:41: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
bowling_test.py:16: in roll_new_game
    game.roll(roll)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <bowling.BowlingGame object at 0x107b98710>, pins = 3

    def roll(self, pins):
        if not isinstance(pins, int) or pins < 0 or pins > 10:
            raise ValueError("pins must be an integer between 0 and 10")
    
        tenth_start = self._first_nine_end()
        if tenth_start is None:
            # A frame among the first nine is in progress.
            if self.rolls and self.rolls[-1] != 10:
                frame_start = len(self.rolls) - 1
                # Locate the start of the current frame by parsing completed frames.
                index = 0
                while index < frame_start:
                    index += 1 if self.rolls[index] == 10 else 2
>               if self.rolls[index] + pins > 10:
                   ^^^^^^^^^^^^^^^^^
E               IndexError: list index out of range

bowling.py:32: IndexError
_______ BowlingTest.test_consecutive_strikes_each_get_the_two_roll_bonus _______

self = <bowling_test.BowlingTest testMethod=test_consecutive_strikes_each_get_the_two_roll_bonus>

    def test_consecutive_strikes_each_get_the_two_roll_bonus(self):
        rolls = [10, 10, 10, 5, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
>       game = self.roll_new_game(rolls)
               ^^^^^^^^^^^^^^^^^^^^^^^^^

bowling_test.py:63: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
bowling_test.py:16: in roll_new_game
    game.roll(roll)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <bowling.BowlingGame object at 0x1074df800>, pins = 0

    def roll(self, pins):
        if not isinstance(pins, int) or pins < 0 or pins > 10:
            raise ValueError("pins must be an integer between 0 and 10")
    
        tenth_start = self._first_nine_end()
        if tenth_start is None:
            # A frame among the first nine is in progress.
            if self.rolls and self.rolls[-1] != 10:
                frame_start = len(self.rolls) - 1
                # Locate the start of the current frame by parsing completed frames.
                index = 0
                while index < frame_start:
                    index += 1 if self.rolls[index] == 10 else 2
>               if self.rolls[index] + pins > 10:
                   ^^^^^^^^^^^^^^^^^
E               IndexError: list index out of range

bowling.py:32: IndexError
_ BowlingTest.test_last_two_strikes_followed_by_only_last_bonus_with_non_strike_points _

self = <bowling_test.BowlingTest testMethod=test_last_two_strikes_followed_by_only_last_bonus_with_non_strike_points>

    def test_last_two_strikes_followed_by_only_last_bonus_with_non_strike_points(self):
        rolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 10, 0, 1]
>       game = self.roll_new_game(rolls)
               ^^^^^^^^^^^^^^^^^^^^^^^^^

bowling_test.py:85: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
bowling_test.py:16: in roll_new_game
    game.roll(roll)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <bowling.BowlingGame object at 0x1074dfd80>, pins = 0

    def roll(self, pins):
        if not isinstance(pins, int) or pins < 0 or pins > 10:
            raise ValueError("pins must be an integer between 0 and 10")
    
        tenth_start = self._first_nine_end()
        if tenth_start is None:
            # A frame among the first nine is in progress.
            if self.rolls and self.rolls[-1] != 10:
                frame_start = len(self.rolls) - 1
                # Locate the start of the current frame by parsing completed frames.
                index = 0
                while index < frame_start:
                    index += 1 if self.rolls[index] == 10 else 2
>               if self.rolls[index] + pins > 10:
                   ^^^^^^^^^^^^^^^^^
E               IndexError: list index out of range

bowling.py:32: IndexError
__ BowlingTest.test_points_scored_in_the_roll_after_a_spare_are_counted_twice __

self = <bowling_test.BowlingTest testMethod=test_points_scored_in_the_roll_after_a_spare_are_counted_twice>

    def test_points_scored_in_the_roll_after_a_spare_are_counted_twice(self):
        rolls = [6, 4, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
>       game = self.roll_new_game(rolls)
               ^^^^^^^^^^^^^^^^^^^^^^^^^

bowling_test.py:36: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
bowling_test.py:16: in roll_new_game
    game.roll(roll)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <bowling.BowlingGame object at 0x107becd70>, pins = 3

    def roll(self, pins):
        if not isinstance(pins, int) or pins < 0 or pins > 10:
            raise ValueError("pins must be an integer between 0 and 10")
    
        tenth_start = self._first_nine_end()
        if tenth_start is None:
            # A frame among the first nine is in progress.
            if self.rolls and self.rolls[-1] != 10:
                frame_start = len(self.rolls) - 1
                # Locate the start of the current frame by parsing completed frames.
                index = 0
                while index < frame_start:
                    index += 1 if self.rolls[index] == 10 else 2
>               if self.rolls[index] + pins > 10:
                   ^^^^^^^^^^^^^^^^^
E               IndexError: list index out of range

bowling.py:32: IndexError
_ BowlingTest.test_points_scored_in_the_two_rolls_after_a_strike_are_counted_twice_as_a_bonus _

self = <bowling_test.BowlingTest testMethod=test_points_scored_in_the_two_rolls_after_a_strike_are_counted_twice_as_a_bonus>

    def test_points_scored_in_the_two_rolls_after_a_strike_are_counted_twice_as_a_bonus(
        self,
    ):
        rolls = [10, 5, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
>       game = self.roll_new_game(rolls)
               ^^^^^^^^^^^^^^^^^^^^^^^^^

bowling_test.py:58: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
bowling_test.py:16: in roll_new_game
    game.roll(roll)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <bowling.BowlingGame object at 0x107beca50>, pins = 0

    def roll(self, pins):
        if not isinstance(pins, int) or pins < 0 or pins > 10:
            raise ValueError("pins must be an integer between 0 and 10")
    
        tenth_start = self._first_nine_end()
        if tenth_start is None:
            # A frame among the first nine is in progress.
            if self.rolls and self.rolls[-1] != 10:
                frame_start = len(self.rolls) - 1
                # Locate the start of the current frame by parsing completed frames.
                index = 0
                while index < frame_start:
                    index += 1 if self.rolls[index] == 10 else 2
>               if self.rolls[index] + pins > 10:
                   ^^^^^^^^^^^^^^^^^
E               IndexError: list index out of range

bowling.py:32: IndexError
_ BowlingTest.test_rolling_a_spare_with_the_two_roll_bonus_does_not_get_a_bonus_roll _

self = <bowling_test.BowlingTest testMethod=test_rolling_a_spare_with_the_two_roll_bonus_does_not_get_a_bonus_roll>

    def test_rolling_a_spare_with_the_two_roll_bonus_does_not_get_a_bonus_roll(self):
        rolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 7, 3]
>       game = self.roll_new_game(rolls)
               ^^^^^^^^^^^^^^^^^^^^^^^^^

bowling_test.py:75: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
bowling_test.py:16: in roll_new_game
    game.roll(roll)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <bowling.BowlingGame object at 0x1074ebc80>, pins = 0

    def roll(self, pins):
        if not isinstance(pins, int) or pins < 0 or pins > 10:
            raise ValueError("pins must be an integer between 0 and 10")
    
        tenth_start = self._first_nine_end()
        if tenth_start is None:
            # A frame among the first nine is in progress.
            if self.rolls and self.rolls[-1] != 10:
                frame_start = len(self.rolls) - 1
                # Locate the start of the current frame by parsing completed frames.
                index = 0
                while index < frame_start:
                    index += 1 if self.rolls[index] == 10 else 2
>               if self.rolls[index] + pins > 10:
                   ^^^^^^^^^^^^^^^^^
E               IndexError: list index out of range

bowling.py:32: IndexError
_ BowlingTest.test_second_bonus_roll_after_a_strike_in_the_last_frame_cannot_score_more_than_10_points _

self = <bowling_test.BowlingTest testMethod=test_second_bonus_roll_after_a_strike_in_the_last_frame_cannot_score_more_than_10_points>

    def test_second_bonus_roll_after_a_strike_in_the_last_frame_cannot_score_more_than_10_points(
        self,
    ):
        rolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 10]
>       game = self.roll_new_game(rolls)
               ^^^^^^^^^^^^^^^^^^^^^^^^^

bowling_test.py:153: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
bowling_test.py:16: in roll_new_game
    game.roll(roll)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <bowling.BowlingGame object at 0x107c18f50>, pins = 0

    def roll(self, pins):
        if not isinstance(pins, int) or pins < 0 or pins > 10:
            raise ValueError("pins must be an integer between 0 and 10")
    
        tenth_start = self._first_nine_end()
        if tenth_start is None:
            # A frame among the first nine is in progress.
            if self.rolls and self.rolls[-1] != 10:
                frame_start = len(self.rolls) - 1
                # Locate the start of the current frame by parsing completed frames.
                index = 0
                while index < frame_start:
                    index += 1 if self.rolls[index] == 10 else 2
>               if self.rolls[index] + pins > 10:
                   ^^^^^^^^^^^^^^^^^
E               IndexError: list index out of range

bowling.py:32: IndexError
________ BowlingTest.test_should_be_able_to_score_a_game_with_all_zeros ________

self = <bowling_test.BowlingTest testMethod=test_should_be_able_to_score_a_game_with_all_zeros>

    def test_should_be_able_to_score_a_game_with_all_zeros(self):
        rolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
>       game = self.roll_new_game(rolls)
               ^^^^^^^^^^^^^^^^^^^^^^^^^

bowling_test.py:21: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
bowling_test.py:16: in roll_new_game
    game.roll(roll)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <bowling.BowlingGame object at 0x107b4d710>, pins = 0

    def roll(self, pins):
        if not isinstance(pins, int) or pins < 0 or pins > 10:
            raise ValueError("pins must be an integer between 0 and 10")
    
        tenth_start = self._first_nine_end()
        if tenth_start is None:
            # A frame among the first nine is in progress.
            if self.rolls and self.rolls[-1] != 10:
                frame_start = len(self.rolls) - 1
                # Locate the start of the current frame by parsing completed frames.
                index = 0
                while index < frame_start:
                    index += 1 if self.rolls[index] == 10 else 2
>               if self.rolls[index] + pins > 10:
                   ^^^^^^^^^^^^^^^^^
E               IndexError: list index out of range

bowling.py:32: IndexError
__ BowlingTest.test_should_be_able_to_score_a_game_with_no_strikes_or_spares ___

self = <bowling_test.BowlingTest testMethod=test_should_be_able_to_score_a_game_with_no_strikes_or_spares>

    def test_should_be_able_to_score_a_game_with_no_strikes_or_spares(self):
        rolls = [3, 6, 3, 6, 3, 6, 3, 6, 3, 6, 3, 6, 3, 6, 3, 6, 3, 6, 3, 6]
>       game = self.roll_new_game(rolls)
               ^^^^^^^^^^^^^^^^^^^^^^^^^

bowling_test.py:26: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
bowling_test.py:16: in roll_new_game
    game.roll(roll)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <bowling.BowlingGame object at 0x107be02f0>, pins = 3

    def roll(self, pins):
        if not isinstance(pins, int) or pins < 0 or pins > 10:
            raise ValueError("pins must be an integer between 0 and 10")
    
        tenth_start = self._first_nine_end()
        if tenth_start is None:
            # A frame among the first nine is in progress.
            if self.rolls and self.rolls[-1] != 10:
                frame_start = len(self.rolls) - 1
                # Locate the start of the current frame by parsing completed frames.
                index = 0
                while index < frame_start:
                    index += 1 if self.rolls[index] == 10 else 2
>               if self.rolls[index] + pins > 10:
                   ^^^^^^^^^^^^^^^^^
E               IndexError: list index out of range

bowling.py:32: IndexError
___ BowlingTest.test_strikes_with_the_two_roll_bonus_do_not_get_bonus_rolls ____

self = <bowling_test.BowlingTest testMethod=test_strikes_with_the_two_roll_bonus_do_not_get_bonus_rolls>

    def test_strikes_with_the_two_roll_bonus_do_not_get_bonus_rolls(self):
        rolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 10, 10]
>       game = self.roll_new_game(rolls)
               ^^^^^^^^^^^^^^^^^^^^^^^^^

bowling_test.py:80: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
bowling_test.py:16: in roll_new_game
    game.roll(roll)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <bowling.BowlingGame object at 0x107bb10d0>, pins = 0

    def roll(self, pins):
        if not isinstance(pins, int) or pins < 0 or pins > 10:
            raise ValueError("pins must be an integer between 0 and 10")
    
        tenth_start = self._first_nine_end()
        if tenth_start is None:
            # A frame among the first nine is in progress.
            if self.rolls and self.rolls[-1] != 10:
                frame_start = len(self.rolls) - 1
                # Locate the start of the current frame by parsing completed frames.
                index = 0
                while index < frame_start:
                    index += 1 if self.rolls[index] == 10 else 2
>               if self.rolls[index] + pins > 10:
                   ^^^^^^^^^^^^^^^^^
E               IndexError: list index out of range

bowling.py:32: IndexError
_ BowlingTest.test_the_second_bonus_rolls_after_a_strike_in_the_last_frame_cannot_be_a_strike_if_the_first_one_is_not_a_strike _

self = <bowling_test.BowlingTest testMethod=test_the_second_bonus_rolls_after_a_strike_in_the_last_frame_cannot_be_a_strike_if_the_first_one_is_not_a_strike>

    def test_the_second_bonus_rolls_after_a_strike_in_the_last_frame_cannot_be_a_strike_if_the_first_one_is_not_a_strike(
        self,
    ):
        rolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 6]
>       game = self.roll_new_game(rolls)
               ^^^^^^^^^^^^^^^^^^^^^^^^^

bowling_test.py:145: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
bowling_test.py:16: in roll_new_game
    game.roll(roll)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <bowling.BowlingGame object at 0x107bb1610>, pins = 0

    def roll(self, pins):
        if not isinstance(pins, int) or pins < 0 or pins > 10:
            raise ValueError("pins must be an integer between 0 and 10")
    
        tenth_start = self._first_nine_end()
        if tenth_start is None:
            # A frame among the first nine is in progress.
            if self.rolls and self.rolls[-1] != 10:
                frame_start = len(self.rolls) - 1
                # Locate the start of the current frame by parsing completed frames.
                index = 0
                while index < frame_start:
                    index += 1 if self.rolls[index] == 10 else 2
>               if self.rolls[index] + pins > 10:
                   ^^^^^^^^^^^^^^^^^
E               IndexError: list index out of range

bowling.py:32: IndexError
_ BowlingTest.test_two_bonus_rolls_after_a_strike_in_the_last_frame_can_score_more_than_10_points_if_one_is_a_strike _

self = <bowling_test.BowlingTest testMethod=test_two_bonus_rolls_after_a_strike_in_the_last_frame_can_score_more_than_10_points_if_one_is_a_strike>

    def test_two_bonus_rolls_after_a_strike_in_the_last_frame_can_score_more_than_10_points_if_one_is_a_strike(
        self,
    ):
        rolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 10, 6]
>       game = self.roll_new_game(rolls)
               ^^^^^^^^^^^^^^^^^^^^^^^^^

bowling_test.py:138: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
bowling_test.py:16: in roll_new_game
    game.roll(roll)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <bowling.BowlingGame object at 0x107c29950>, pins = 0

    def roll(self, pins):
        if not isinstance(pins, int) or pins < 0 or pins > 10:
            raise ValueError("pins must be an integer between 0 and 10")
    
        tenth_start = self._first_nine_end()
        if tenth_start is None:
            # A frame among the first nine is in progress.
            if self.rolls and self.rolls[-1] != 10:
                frame_start = len(self.rolls) - 1
                # Locate the start of the current frame by parsing completed frames.
                index = 0
                while index < frame_start:
                    index += 1 if self.rolls[index] == 10 else 2
>               if self.rolls[index] + pins > 10:
                   ^^^^^^^^^^^^^^^^^
E               IndexError: list index out of range

bowling.py:32: IndexError
_ BowlingTest.test_two_bonus_rolls_after_a_strike_in_the_last_frame_cannot_score_more_than_10_points _

self = <bowling_test.BowlingTest testMethod=test_two_bonus_rolls_after_a_strike_in_the_last_frame_cannot_score_more_than_10_points>

    def test_two_bonus_rolls_after_a_strike_in_the_last_frame_cannot_score_more_than_10_points(
        self,
    ):
        rolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 5]
>       game = self.roll_new_game(rolls)
               ^^^^^^^^^^^^^^^^^^^^^^^^^

bowling_test.py:130: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
bowling_test.py:16: in roll_new_game
    game.roll(roll)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <bowling.BowlingGame object at 0x107c29c70>, pins = 0

    def roll(self, pins):
        if not isinstance(pins, int) or pins < 0 or pins > 10:
            raise ValueError("pins must be an integer between 0 and 10")
    
        tenth_start = self._first_nine_end()
        if tenth_start is None:
            # A frame among the first nine is in progress.
            if self.rolls and self.rolls[-1] != 10:
                frame_start = len(self.rolls) - 1
                # Locate the start of the current frame by parsing completed frames.
                index = 0
                while index < frame_start:
                    index += 1 if self.rolls[index] == 10 else 2
>               if self.rolls[index] + pins > 10:
                   ^^^^^^^^^^^^^^^^^
E               IndexError: list index out of range

bowling.py:32: IndexError
=========================== short test summary info ============================
FAILED bowling_test.py::BowlingTest::test_a_spare_followed_by_zeros_is_worth_ten_points
FAILED bowling_test.py::BowlingTest::test_a_spare_in_the_last_frame_gets_a_one_roll_bonus_that_is_counted_once
FAILED bowling_test.py::BowlingTest::test_a_strike_earns_ten_points_in_a_frame_with_a_single_roll
FAILED bowling_test.py::BowlingTest::test_a_strike_in_the_last_frame_gets_a_two_roll_bonus_that_is_counted_once
FAILED bowling_test.py::BowlingTest::test_a_strike_with_the_one_roll_bonus_after_a_spare_in_the_last_frame_does_not_get_a_bonus
FAILED bowling_test.py::BowlingTest::test_bonus_roll_after_a_strike_in_the_last_frame_cannot_score_more_than_10_points
FAILED bowling_test.py::BowlingTest::test_bonus_roll_for_a_spare_in_the_last_frame_must_be_rolled_before_score_can_be_calculated
FAILED bowling_test.py::BowlingTest::test_bonus_rolls_for_a_strike_in_the_last_frame_must_be_rolled_before_score_can_be_calculated
FAILED bowling_test.py::BowlingTest::test_both_bonus_rolls_for_a_strike_in_the_last_frame_must_be_rolled_before_score_can_be_calculated
FAILED bowling_test.py::BowlingTest::test_cannot_roll_after_bonus_roll_for_spare
FAILED bowling_test.py::BowlingTest::test_cannot_roll_after_bonus_rolls_for_strike
FAILED bowling_test.py::BowlingTest::test_cannot_roll_if_game_already_has_ten_frames
FAILED bowling_test.py::BowlingTest::test_consecutive_spares_each_get_a_one_roll_bonus
FAILED bowling_test.py::BowlingTest::test_consecutive_strikes_each_get_the_two_roll_bonus
FAILED bowling_test.py::BowlingTest::test_last_two_strikes_followed_by_only_last_bonus_with_non_strike_points
FAILED bowling_test.py::BowlingTest::test_points_scored_in_the_roll_after_a_spare_are_counted_twice
FAILED bowling_test.py::BowlingTest::test_points_scored_in_the_two_rolls_after_a_strike_are_counted_twice_as_a_bonus
FAILED bowling_test.py::BowlingTest::test_rolling_a_spare_with_the_two_roll_bonus_does_not_get_a_bonus_roll
FAILED bowling_test.py::BowlingTest::test_second_bonus_roll_after_a_strike_in_the_last_frame_cannot_score_more_than_10_points
FAILED bowling_test.py::BowlingTest::test_should_be_able_to_score_a_game_with_all_zeros
FAILED bowling_test.py::BowlingTest::test_should_be_able_to_score_a_game_with_no_strikes_or_spares
FAILED bowling_test.py::BowlingTest::test_strikes_with_the_two_roll_bonus_do_not_get_bonus_rolls
FAILED bowling_test.py::BowlingTest::test_the_second_bonus_rolls_after_a_strike_in_the_last_frame_cannot_be_a_strike_if_the_first_one_is_not_a_strike
FAILED bowling_test.py::BowlingTest::test_two_bonus_rolls_after_a_strike_in_the_last_frame_can_score_more_than_10_points_if_one_is_a_strike
FAILED bowling_test.py::BowlingTest::test_two_bonus_rolls_after_a_strike_in_the_last_frame_cannot_score_more_than_10_points
25 failed, 6 passed in 0.16s


Command exited with code 1
```

</details>

**Reply:**

→ tool `edit`

```
{
 "path": "bowling.py",
 "edits": [
  {
   "oldText": "        for _ in range(9):\n            if index >= len(self.rolls):\n                return None\n            if self.rolls[index] == 10:\n                index += 1\n            else:\n                if index + 1 >= len(self.rolls):\n                    return None\n                index += 2\n        return index",
   "newText": "        for frame in range(9):\n            if index >= len(self.rolls):\n                return index if frame == 9 else None\n            if self.rolls[index] == 10:\n                index += 1\n            else:\n                if index + 1 >= len(self.rolls):\n                    return None\n                index += 2\n        return index"
  }
 ]
}
```

## Call 6 · main agent

21,902 in (21,483 cached) · 78 out · $0.0003 · 3082 ms · OpenRouter id `gen-1793672232-jCNC37CA7WSWjAlRaiaw`

**New in this request** (continues call 5):

**assistant → tool `edit`**

```
{
 "path": "bowling.py",
 "edits": [
  {
   "oldText": "        for _ in range(9):\n            if index >= len(self.rolls):\n                return None\n            if self.rolls[index] == 10:\n                index += 1\n            else:\n                if index + 1 >= len(self.rolls):\n                    return None\n                index += 2\n        return index",
   "newText": "        for frame in range(9):\n            if index >= len(self.rolls):\n                return index if frame == 9 else None\n            if self.rolls[index] == 10:\n                index += 1\n            else:\n                if index + 1 >= len(self.rolls):\n                    return None\n                index += 2\n        return index"
  }
 ]
}
```

**tool result** (`call_usVHu5s06g4FzaW5FuKpLbQD`)

```
Successfully replaced 1 block(s) in bowling.py.
```

**Reply:**

*reasoning:* **Investigating loop conditions**

I'm considering a scenario where there's an impossible loop when frame equals 9. It seems if the ninth frame is missing after 8, the output should be none. However, if the tenth index returns correctly after the loop, that could be fine. It's puzzling that the incomplete tenth starting without a roll gives me an index length that makes sense. So, I need to run it through and see what happens!

→ tool `bash`

```
{
 "command": "python3 -m pytest -q",
 "timeout": 120000
}
```

## Call 7 · main agent

34,715 in (21,899 cached) · 807 out · $0.0022 · 10033 ms · OpenRouter id `gen-1793672235-dvADVjFiVjxKTEj3VotR`

**New in this request** (continues call 6):

**assistant → tool `bash`**

```
{
 "command": "python3 -m pytest -q",
 "timeout": 120000
}
```

**tool result** (`call_Cf85quBbxJGhis07tj7pfThR`)

<details><summary>929 lines</summary>

```
.FFFFF...FFFFFFFFFFFFF.FFFFFFF.                                          [100%]
=================================== FAILURES ===================================
________ BowlingTest.test_a_spare_followed_by_zeros_is_worth_ten_points ________

self = <bowling_test.BowlingTest testMethod=test_a_spare_followed_by_zeros_is_worth_ten_points>

    def test_a_spare_followed_by_zeros_is_worth_ten_points(self):
        rolls = [6, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
>       game = self.roll_new_game(rolls)
               ^^^^^^^^^^^^^^^^^^^^^^^^^

bowling_test.py:31: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
bowling_test.py:16: in roll_new_game
    game.roll(roll)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <bowling.BowlingGame object at 0x105af1090>, pins = 0

    def roll(self, pins):
        if not isinstance(pins, int) or pins < 0 or pins > 10:
            raise ValueError("pins must be an integer between 0 and 10")
    
        tenth_start = self._first_nine_end()
        if tenth_start is None:
            # A frame among the first nine is in progress.
            if self.rolls and self.rolls[-1] != 10:
                frame_start = len(self.rolls) - 1
                # Locate the start of the current frame by parsing completed frames.
                index = 0
                while index < frame_start:
                    index += 1 if self.rolls[index] == 10 else 2
>               if self.rolls[index] + pins > 10:
                   ^^^^^^^^^^^^^^^^^
E               IndexError: list index out of range

bowling.py:32: IndexError
_ BowlingTest.test_a_spare_in_the_last_frame_gets_a_one_roll_bonus_that_is_counted_once _

self = <bowling_test.BowlingTest testMethod=test_a_spare_in_the_last_frame_gets_a_one_roll_bonus_that_is_counted_once>

    def test_a_spare_in_the_last_frame_gets_a_one_roll_bonus_that_is_counted_once(self):
        rolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 3, 7]
>       game = self.roll_new_game(rolls)
               ^^^^^^^^^^^^^^^^^^^^^^^^^

bowling_test.py:46: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
bowling_test.py:16: in roll_new_game
    game.roll(roll)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <bowling.BowlingGame object at 0x105af3ed0>, pins = 0

    def roll(self, pins):
        if not isinstance(pins, int) or pins < 0 or pins > 10:
            raise ValueError("pins must be an integer between 0 and 10")
    
        tenth_start = self._first_nine_end()
        if tenth_start is None:
            # A frame among the first nine is in progress.
            if self.rolls and self.rolls[-1] != 10:
                frame_start = len(self.rolls) - 1
                # Locate the start of the current frame by parsing completed frames.
                index = 0
                while index < frame_start:
                    index += 1 if self.rolls[index] == 10 else 2
>               if self.rolls[index] + pins > 10:
                   ^^^^^^^^^^^^^^^^^
E               IndexError: list index out of range

bowling.py:32: IndexError
___ BowlingTest.test_a_strike_earns_ten_points_in_a_frame_with_a_single_roll ___

self = <bowling_test.BowlingTest testMethod=test_a_strike_earns_ten_points_in_a_frame_with_a_single_roll>

    def test_a_strike_earns_ten_points_in_a_frame_with_a_single_roll(self):
        rolls = [10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
>       game = self.roll_new_game(rolls)
               ^^^^^^^^^^^^^^^^^^^^^^^^^

bowling_test.py:51: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
bowling_test.py:16: in roll_new_game
    game.roll(roll)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <bowling.BowlingGame object at 0x105a82650>, pins = 0

    def roll(self, pins):
        if not isinstance(pins, int) or pins < 0 or pins > 10:
            raise ValueError("pins must be an integer between 0 and 10")
    
        tenth_start = self._first_nine_end()
        if tenth_start is None:
            # A frame among the first nine is in progress.
            if self.rolls and self.rolls[-1] != 10:
                frame_start = len(self.rolls) - 1
                # Locate the start of the current frame by parsing completed frames.
                index = 0
                while index < frame_start:
                    index += 1 if self.rolls[index] == 10 else 2
>               if self.rolls[index] + pins > 10:
                   ^^^^^^^^^^^^^^^^^
E               IndexError: list index out of range

bowling.py:32: IndexError
_ BowlingTest.test_a_strike_in_the_last_frame_gets_a_two_roll_bonus_that_is_counted_once _

self = <bowling_test.BowlingTest testMethod=test_a_strike_in_the_last_frame_gets_a_two_roll_bonus_that_is_counted_once>

    def test_a_strike_in_the_last_frame_gets_a_two_roll_bonus_that_is_counted_once(
        self,
    ):
        rolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 7, 1]
>       game = self.roll_new_game(rolls)
               ^^^^^^^^^^^^^^^^^^^^^^^^^

bowling_test.py:70: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
bowling_test.py:16: in roll_new_game
    game.roll(roll)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <bowling.BowlingGame object at 0x105a829e0>, pins = 0

    def roll(self, pins):
        if not isinstance(pins, int) or pins < 0 or pins > 10:
            raise ValueError("pins must be an integer between 0 and 10")
    
        tenth_start = self._first_nine_end()
        if tenth_start is None:
            # A frame among the first nine is in progress.
            if self.rolls and self.rolls[-1] != 10:
                frame_start = len(self.rolls) - 1
                # Locate the start of the current frame by parsing completed frames.
                index = 0
                while index < frame_start:
                    index += 1 if self.rolls[index] == 10 else 2
>               if self.rolls[index] + pins > 10:
                   ^^^^^^^^^^^^^^^^^
E               IndexError: list index out of range

bowling.py:32: IndexError
_ BowlingTest.test_a_strike_with_the_one_roll_bonus_after_a_spare_in_the_last_frame_does_not_get_a_bonus _

self = <bowling_test.BowlingTest testMethod=test_a_strike_with_the_one_roll_bonus_after_a_spare_in_the_last_frame_does_not_get_a_bonus>

    def test_a_strike_with_the_one_roll_bonus_after_a_spare_in_the_last_frame_does_not_get_a_bonus(
        self,
    ):
        rolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 3, 10]
>       game = self.roll_new_game(rolls)
               ^^^^^^^^^^^^^^^^^^^^^^^^^

bowling_test.py:92: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
bowling_test.py:16: in roll_new_game
    game.roll(roll)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <bowling.BowlingGame object at 0x105d18ef0>, pins = 0

    def roll(self, pins):
        if not isinstance(pins, int) or pins < 0 or pins > 10:
            raise ValueError("pins must be an integer between 0 and 10")
    
        tenth_start = self._first_nine_end()
        if tenth_start is None:
            # A frame among the first nine is in progress.
            if self.rolls and self.rolls[-1] != 10:
                frame_start = len(self.rolls) - 1
                # Locate the start of the current frame by parsing completed frames.
                index = 0
                while index < frame_start:
                    index += 1 if self.rolls[index] == 10 else 2
>               if self.rolls[index] + pins > 10:
                   ^^^^^^^^^^^^^^^^^
E               IndexError: list index out of range

bowling.py:32: IndexError
_ BowlingTest.test_bonus_roll_after_a_strike_in_the_last_frame_cannot_score_more_than_10_points _

self = <bowling_test.BowlingTest testMethod=test_bonus_roll_after_a_strike_in_the_last_frame_cannot_score_more_than_10_points>

    def test_bonus_roll_after_a_strike_in_the_last_frame_cannot_score_more_than_10_points(
        self,
    ):
        rolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10]
>       game = self.roll_new_game(rolls)
               ^^^^^^^^^^^^^^^^^^^^^^^^^

bowling_test.py:122: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
bowling_test.py:16: in roll_new_game
    game.roll(roll)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <bowling.BowlingGame object at 0x105d90150>, pins = 0

    def roll(self, pins):
        if not isinstance(pins, int) or pins < 0 or pins > 10:
            raise ValueError("pins must be an integer between 0 and 10")
    
        tenth_start = self._first_nine_end()
        if tenth_start is None:
            # A frame among the first nine is in progress.
            if self.rolls and self.rolls[-1] != 10:
                frame_start = len(self.rolls) - 1
                # Locate the start of the current frame by parsing completed frames.
                index = 0
                while index < frame_start:
                    index += 1 if self.rolls[index] == 10 else 2
>               if self.rolls[index] + pins > 10:
                   ^^^^^^^^^^^^^^^^^
E               IndexError: list index out of range

bowling.py:32: IndexError
_ BowlingTest.test_bonus_roll_for_a_spare_in_the_last_frame_must_be_rolled_before_score_can_be_calculated _

self = <bowling_test.BowlingTest testMethod=test_bonus_roll_for_a_spare_in_the_last_frame_must_be_rolled_before_score_can_be_calculated>

    def test_bonus_roll_for_a_spare_in_the_last_frame_must_be_rolled_before_score_can_be_calculated(
        self,
    ):
        rolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 3]
>       game = self.roll_new_game(rolls)
               ^^^^^^^^^^^^^^^^^^^^^^^^^

bowling_test.py:195: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
bowling_test.py:16: in roll_new_game
    game.roll(roll)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <bowling.BowlingGame object at 0x105da5400>, pins = 0

    def roll(self, pins):
        if not isinstance(pins, int) or pins < 0 or pins > 10:
            raise ValueError("pins must be an integer between 0 and 10")
    
        tenth_start = self._first_nine_end()
        if tenth_start is None:
            # A frame among the first nine is in progress.
            if self.rolls and self.rolls[-1] != 10:
                frame_start = len(self.rolls) - 1
                # Locate the start of the current frame by parsing completed frames.
                index = 0
                while index < frame_start:
                    index += 1 if self.rolls[index] == 10 else 2
>               if self.rolls[index] + pins > 10:
                   ^^^^^^^^^^^^^^^^^
E               IndexError: list index out of range

bowling.py:32: IndexError
_ BowlingTest.test_bonus_rolls_for_a_strike_in_the_last_frame_must_be_rolled_before_score_can_be_calculated _

self = <bowling_test.BowlingTest testMethod=test_bonus_rolls_for_a_strike_in_the_last_frame_must_be_rolled_before_score_can_be_calculated>

    def test_bonus_rolls_for_a_strike_in_the_last_frame_must_be_rolled_before_score_can_be_calculated(
        self,
    ):
        rolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10]
>       game = self.roll_new_game(rolls)
               ^^^^^^^^^^^^^^^^^^^^^^^^^

bowling_test.py:179: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
bowling_test.py:16: in roll_new_game
    game.roll(roll)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <bowling.BowlingGame object at 0x105a17890>, pins = 0

    def roll(self, pins):
        if not isinstance(pins, int) or pins < 0 or pins > 10:
            raise ValueError("pins must be an integer between 0 and 10")
    
        tenth_start = self._first_nine_end()
        if tenth_start is None:
            # A frame among the first nine is in progress.
            if self.rolls and self.rolls[-1] != 10:
                frame_start = len(self.rolls) - 1
                # Locate the start of the current frame by parsing completed frames.
                index = 0
                while index < frame_start:
                    index += 1 if self.rolls[index] == 10 else 2
>               if self.rolls[index] + pins > 10:
                   ^^^^^^^^^^^^^^^^^
E               IndexError: list index out of range

bowling.py:32: IndexError
_ BowlingTest.test_both_bonus_rolls_for_a_strike_in_the_last_frame_must_be_rolled_before_score_can_be_calculated _

self = <bowling_test.BowlingTest testMethod=test_both_bonus_rolls_for_a_strike_in_the_last_frame_must_be_rolled_before_score_can_be_calculated>

    def test_both_bonus_rolls_for_a_strike_in_the_last_frame_must_be_rolled_before_score_can_be_calculated(
        self,
    ):
        rolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 10]
>       game = self.roll_new_game(rolls)
               ^^^^^^^^^^^^^^^^^^^^^^^^^

bowling_test.py:187: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
bowling_test.py:16: in roll_new_game
    game.roll(roll)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <bowling.BowlingGame object at 0x105d165f0>, pins = 0

    def roll(self, pins):
        if not isinstance(pins, int) or pins < 0 or pins > 10:
            raise ValueError("pins must be an integer between 0 and 10")
    
        tenth_start = self._first_nine_end()
        if tenth_start is None:
            # A frame among the first nine is in progress.
            if self.rolls and self.rolls[-1] != 10:
                frame_start = len(self.rolls) - 1
                # Locate the start of the current frame by parsing completed frames.
                index = 0
                while index < frame_start:
                    index += 1 if self.rolls[index] == 10 else 2
>               if self.rolls[index] + pins > 10:
                   ^^^^^^^^^^^^^^^^^
E               IndexError: list index out of range

bowling.py:32: IndexError
___________ BowlingTest.test_cannot_roll_after_bonus_roll_for_spare ____________

self = <bowling_test.BowlingTest testMethod=test_cannot_roll_after_bonus_roll_for_spare>

    def test_cannot_roll_after_bonus_roll_for_spare(self):
        rolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 3, 2]
>       game = self.roll_new_game(rolls)
               ^^^^^^^^^^^^^^^^^^^^^^^^^

bowling_test.py:201: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
bowling_test.py:16: in roll_new_game
    game.roll(roll)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <bowling.BowlingGame object at 0x105d15c50>, pins = 0

    def roll(self, pins):
        if not isinstance(pins, int) or pins < 0 or pins > 10:
            raise ValueError("pins must be an integer between 0 and 10")
    
        tenth_start = self._first_nine_end()
        if tenth_start is None:
            # A frame among the first nine is in progress.
            if self.rolls and self.rolls[-1] != 10:
                frame_start = len(self.rolls) - 1
                # Locate the start of the current frame by parsing completed frames.
                index = 0
                while index < frame_start:
                    index += 1 if self.rolls[index] == 10 else 2
>               if self.rolls[index] + pins > 10:
                   ^^^^^^^^^^^^^^^^^
E               IndexError: list index out of range

bowling.py:32: IndexError
__________ BowlingTest.test_cannot_roll_after_bonus_rolls_for_strike ___________

self = <bowling_test.BowlingTest testMethod=test_cannot_roll_after_bonus_rolls_for_strike>

    def test_cannot_roll_after_bonus_rolls_for_strike(self):
        rolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 3, 2]
>       game = self.roll_new_game(rolls)
               ^^^^^^^^^^^^^^^^^^^^^^^^^

bowling_test.py:207: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
bowling_test.py:16: in roll_new_game
    game.roll(roll)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <bowling.BowlingGame object at 0x105dd2340>, pins = 0

    def roll(self, pins):
        if not isinstance(pins, int) or pins < 0 or pins > 10:
            raise ValueError("pins must be an integer between 0 and 10")
    
        tenth_start = self._first_nine_end()
        if tenth_start is None:
            # A frame among the first nine is in progress.
            if self.rolls and self.rolls[-1] != 10:
                frame_start = len(self.rolls) - 1
                # Locate the start of the current frame by parsing completed frames.
                index = 0
                while index < frame_start:
                    index += 1 if self.rolls[index] == 10 else 2
>               if self.rolls[index] + pins > 10:
                   ^^^^^^^^^^^^^^^^^
E               IndexError: list index out of range

bowling.py:32: IndexError
_________ BowlingTest.test_cannot_roll_if_game_already_has_ten_frames __________

self = <bowling_test.BowlingTest testMethod=test_cannot_roll_if_game_already_has_ten_frames>

    def test_cannot_roll_if_game_already_has_ten_frames(self):
        rolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
>       game = self.roll_new_game(rolls)
               ^^^^^^^^^^^^^^^^^^^^^^^^^

bowling_test.py:171: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
bowling_test.py:16: in roll_new_game
    game.roll(roll)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <bowling.BowlingGame object at 0x105d501d0>, pins = 0

    def roll(self, pins):
        if not isinstance(pins, int) or pins < 0 or pins > 10:
            raise ValueError("pins must be an integer between 0 and 10")
    
        tenth_start = self._first_nine_end()
        if tenth_start is None:
            # A frame among the first nine is in progress.
            if self.rolls and self.rolls[-1] != 10:
                frame_start = len(self.rolls) - 1
                # Locate the start of the current frame by parsing completed frames.
                index = 0
                while index < frame_start:
                    index += 1 if self.rolls[index] == 10 else 2
>               if self.rolls[index] + pins > 10:
                   ^^^^^^^^^^^^^^^^^
E               IndexError: list index out of range

bowling.py:32: IndexError
________ BowlingTest.test_consecutive_spares_each_get_a_one_roll_bonus _________

self = <bowling_test.BowlingTest testMethod=test_consecutive_spares_each_get_a_one_roll_bonus>

    def test_consecutive_spares_each_get_a_one_roll_bonus(self):
        rolls = [5, 5, 3, 7, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
>       game = self.roll_new_game(rolls)
               ^^^^^^^^^^^^^^^^^^^^^^^^^

bowling_test.py:41: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
bowling_test.py:16: in roll_new_game
    game.roll(roll)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <bowling.BowlingGame object at 0x105d50290>, pins = 3

    def roll(self, pins):
        if not isinstance(pins, int) or pins < 0 or pins > 10:
            raise ValueError("pins must be an integer between 0 and 10")
    
        tenth_start = self._first_nine_end()
        if tenth_start is None:
            # A frame among the first nine is in progress.
            if self.rolls and self.rolls[-1] != 10:
                frame_start = len(self.rolls) - 1
                # Locate the start of the current frame by parsing completed frames.
                index = 0
                while index < frame_start:
                    index += 1 if self.rolls[index] == 10 else 2
>               if self.rolls[index] + pins > 10:
                   ^^^^^^^^^^^^^^^^^
E               IndexError: list index out of range

bowling.py:32: IndexError
_______ BowlingTest.test_consecutive_strikes_each_get_the_two_roll_bonus _______

self = <bowling_test.BowlingTest testMethod=test_consecutive_strikes_each_get_the_two_roll_bonus>

    def test_consecutive_strikes_each_get_the_two_roll_bonus(self):
        rolls = [10, 10, 10, 5, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
>       game = self.roll_new_game(rolls)
               ^^^^^^^^^^^^^^^^^^^^^^^^^

bowling_test.py:63: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
bowling_test.py:16: in roll_new_game
    game.roll(roll)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <bowling.BowlingGame object at 0x105de8310>, pins = 0

    def roll(self, pins):
        if not isinstance(pins, int) or pins < 0 or pins > 10:
            raise ValueError("pins must be an integer between 0 and 10")
    
        tenth_start = self._first_nine_end()
        if tenth_start is None:
            # A frame among the first nine is in progress.
            if self.rolls and self.rolls[-1] != 10:
                frame_start = len(self.rolls) - 1
                # Locate the start of the current frame by parsing completed frames.
                index = 0
                while index < frame_start:
                    index += 1 if self.rolls[index] == 10 else 2
>               if self.rolls[index] + pins > 10:
                   ^^^^^^^^^^^^^^^^^
E               IndexError: list index out of range

bowling.py:32: IndexError
_ BowlingTest.test_last_two_strikes_followed_by_only_last_bonus_with_non_strike_points _

self = <bowling_test.BowlingTest testMethod=test_last_two_strikes_followed_by_only_last_bonus_with_non_strike_points>

    def test_last_two_strikes_followed_by_only_last_bonus_with_non_strike_points(self):
        rolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 10, 0, 1]
>       game = self.roll_new_game(rolls)
               ^^^^^^^^^^^^^^^^^^^^^^^^^

bowling_test.py:85: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
bowling_test.py:16: in roll_new_game
    game.roll(roll)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <bowling.BowlingGame object at 0x105de8680>, pins = 0

    def roll(self, pins):
        if not isinstance(pins, int) or pins < 0 or pins > 10:
            raise ValueError("pins must be an integer between 0 and 10")
    
        tenth_start = self._first_nine_end()
        if tenth_start is None:
            # A frame among the first nine is in progress.
            if self.rolls and self.rolls[-1] != 10:
                frame_start = len(self.rolls) - 1
                # Locate the start of the current frame by parsing completed frames.
                index = 0
                while index < frame_start:
                    index += 1 if self.rolls[index] == 10 else 2
>               if self.rolls[index] + pins > 10:
                   ^^^^^^^^^^^^^^^^^
E               IndexError: list index out of range

bowling.py:32: IndexError
__ BowlingTest.test_points_scored_in_the_roll_after_a_spare_are_counted_twice __

self = <bowling_test.BowlingTest testMethod=test_points_scored_in_the_roll_after_a_spare_are_counted_twice>

    def test_points_scored_in_the_roll_after_a_spare_are_counted_twice(self):
        rolls = [6, 4, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
>       game = self.roll_new_game(rolls)
               ^^^^^^^^^^^^^^^^^^^^^^^^^

bowling_test.py:36: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
bowling_test.py:16: in roll_new_game
    game.roll(roll)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <bowling.BowlingGame object at 0x105dc9270>, pins = 3

    def roll(self, pins):
        if not isinstance(pins, int) or pins < 0 or pins > 10:
            raise ValueError("pins must be an integer between 0 and 10")
    
        tenth_start = self._first_nine_end()
        if tenth_start is None:
            # A frame among the first nine is in progress.
            if self.rolls and self.rolls[-1] != 10:
                frame_start = len(self.rolls) - 1
                # Locate the start of the current frame by parsing completed frames.
                index = 0
                while index < frame_start:
                    index += 1 if self.rolls[index] == 10 else 2
>               if self.rolls[index] + pins > 10:
                   ^^^^^^^^^^^^^^^^^
E               IndexError: list index out of range

bowling.py:32: IndexError
_ BowlingTest.test_points_scored_in_the_two_rolls_after_a_strike_are_counted_twice_as_a_bonus _

self = <bowling_test.BowlingTest testMethod=test_points_scored_in_the_two_rolls_after_a_strike_are_counted_twice_as_a_bonus>

    def test_points_scored_in_the_two_rolls_after_a_strike_are_counted_twice_as_a_bonus(
        self,
    ):
        rolls = [10, 5, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
>       game = self.roll_new_game(rolls)
               ^^^^^^^^^^^^^^^^^^^^^^^^^

bowling_test.py:58: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
bowling_test.py:16: in roll_new_game
    game.roll(roll)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <bowling.BowlingGame object at 0x105dc98b0>, pins = 0

    def roll(self, pins):
        if not isinstance(pins, int) or pins < 0 or pins > 10:
            raise ValueError("pins must be an integer between 0 and 10")
    
        tenth_start = self._first_nine_end()
        if tenth_start is None:
            # A frame among the first nine is in progress.
            if self.rolls and self.rolls[-1] != 10:
                frame_start = len(self.rolls) - 1
                # Locate the start of the current frame by parsing completed frames.
                index = 0
                while index < frame_start:
                    index += 1 if self.rolls[index] == 10 else 2
>               if self.rolls[index] + pins > 10:
                   ^^^^^^^^^^^^^^^^^
E               IndexError: list index out of range

bowling.py:32: IndexError
_ BowlingTest.test_rolling_a_spare_with_the_two_roll_bonus_does_not_get_a_bonus_roll _

self = <bowling_test.BowlingTest testMethod=test_rolling_a_spare_with_the_two_roll_bonus_does_not_get_a_bonus_roll>

    def test_rolling_a_spare_with_the_two_roll_bonus_does_not_get_a_bonus_roll(self):
        rolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 7, 3]
>       game = self.roll_new_game(rolls)
               ^^^^^^^^^^^^^^^^^^^^^^^^^

bowling_test.py:75: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
bowling_test.py:16: in roll_new_game
    game.roll(roll)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <bowling.BowlingGame object at 0x105a5bad0>, pins = 0

    def roll(self, pins):
        if not isinstance(pins, int) or pins < 0 or pins > 10:
            raise ValueError("pins must be an integer between 0 and 10")
    
        tenth_start = self._first_nine_end()
        if tenth_start is None:
            # A frame among the first nine is in progress.
            if self.rolls and self.rolls[-1] != 10:
                frame_start = len(self.rolls) - 1
                # Locate the start of the current frame by parsing completed frames.
                index = 0
                while index < frame_start:
                    index += 1 if self.rolls[index] == 10 else 2
>               if self.rolls[index] + pins > 10:
                   ^^^^^^^^^^^^^^^^^
E               IndexError: list index out of range

bowling.py:32: IndexError
_ BowlingTest.test_second_bonus_roll_after_a_strike_in_the_last_frame_cannot_score_more_than_10_points _

self = <bowling_test.BowlingTest testMethod=test_second_bonus_roll_after_a_strike_in_the_last_frame_cannot_score_more_than_10_points>

    def test_second_bonus_roll_after_a_strike_in_the_last_frame_cannot_score_more_than_10_points(
        self,
    ):
        rolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 10]
>       game = self.roll_new_game(rolls)
               ^^^^^^^^^^^^^^^^^^^^^^^^^

bowling_test.py:153: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
bowling_test.py:16: in roll_new_game
    game.roll(roll)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <bowling.BowlingGame object at 0x105dc16d0>, pins = 0

    def roll(self, pins):
        if not isinstance(pins, int) or pins < 0 or pins > 10:
            raise ValueError("pins must be an integer between 0 and 10")
    
        tenth_start = self._first_nine_end()
        if tenth_start is None:
            # A frame among the first nine is in progress.
            if self.rolls and self.rolls[-1] != 10:
                frame_start = len(self.rolls) - 1
                # Locate the start of the current frame by parsing completed frames.
                index = 0
                while index < frame_start:
                    index += 1 if self.rolls[index] == 10 else 2
>               if self.rolls[index] + pins > 10:
                   ^^^^^^^^^^^^^^^^^
E               IndexError: list index out of range

bowling.py:32: IndexError
________ BowlingTest.test_should_be_able_to_score_a_game_with_all_zeros ________

self = <bowling_test.BowlingTest testMethod=test_should_be_able_to_score_a_game_with_all_zeros>

    def test_should_be_able_to_score_a_game_with_all_zeros(self):
        rolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
>       game = self.roll_new_game(rolls)
               ^^^^^^^^^^^^^^^^^^^^^^^^^

bowling_test.py:21: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
bowling_test.py:16: in roll_new_game
    game.roll(roll)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <bowling.BowlingGame object at 0x105d40a60>, pins = 0

    def roll(self, pins):
        if not isinstance(pins, int) or pins < 0 or pins > 10:
            raise ValueError("pins must be an integer between 0 and 10")
    
        tenth_start = self._first_nine_end()
        if tenth_start is None:
            # A frame among the first nine is in progress.
            if self.rolls and self.rolls[-1] != 10:
                frame_start = len(self.rolls) - 1
                # Locate the start of the current frame by parsing completed frames.
                index = 0
                while index < frame_start:
                    index += 1 if self.rolls[index] == 10 else 2
>               if self.rolls[index] + pins > 10:
                   ^^^^^^^^^^^^^^^^^
E               IndexError: list index out of range

bowling.py:32: IndexError
__ BowlingTest.test_should_be_able_to_score_a_game_with_no_strikes_or_spares ___

self = <bowling_test.BowlingTest testMethod=test_should_be_able_to_score_a_game_with_no_strikes_or_spares>

    def test_should_be_able_to_score_a_game_with_no_strikes_or_spares(self):
        rolls = [3, 6, 3, 6, 3, 6, 3, 6, 3, 6, 3, 6, 3, 6, 3, 6, 3, 6, 3, 6]
>       game = self.roll_new_game(rolls)
               ^^^^^^^^^^^^^^^^^^^^^^^^^

bowling_test.py:26: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
bowling_test.py:16: in roll_new_game
    game.roll(roll)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <bowling.BowlingGame object at 0x105d40670>, pins = 3

    def roll(self, pins):
        if not isinstance(pins, int) or pins < 0 or pins > 10:
            raise ValueError("pins must be an integer between 0 and 10")
    
        tenth_start = self._first_nine_end()
        if tenth_start is None:
            # A frame among the first nine is in progress.
            if self.rolls and self.rolls[-1] != 10:
                frame_start = len(self.rolls) - 1
                # Locate the start of the current frame by parsing completed frames.
                index = 0
                while index < frame_start:
                    index += 1 if self.rolls[index] == 10 else 2
>               if self.rolls[index] + pins > 10:
                   ^^^^^^^^^^^^^^^^^
E               IndexError: list index out of range

bowling.py:32: IndexError
___ BowlingTest.test_strikes_with_the_two_roll_bonus_do_not_get_bonus_rolls ____

self = <bowling_test.BowlingTest testMethod=test_strikes_with_the_two_roll_bonus_do_not_get_bonus_rolls>

    def test_strikes_with_the_two_roll_bonus_do_not_get_bonus_rolls(self):
        rolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 10, 10]
>       game = self.roll_new_game(rolls)
               ^^^^^^^^^^^^^^^^^^^^^^^^^

bowling_test.py:80: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
bowling_test.py:16: in roll_new_game
    game.roll(roll)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <bowling.BowlingGame object at 0x105dd91f0>, pins = 0

    def roll(self, pins):
        if not isinstance(pins, int) or pins < 0 or pins > 10:
            raise ValueError("pins must be an integer between 0 and 10")
    
        tenth_start = self._first_nine_end()
        if tenth_start is None:
            # A frame among the first nine is in progress.
            if self.rolls and self.rolls[-1] != 10:
                frame_start = len(self.rolls) - 1
                # Locate the start of the current frame by parsing completed frames.
                index = 0
                while index < frame_start:
                    index += 1 if self.rolls[index] == 10 else 2
>               if self.rolls[index] + pins > 10:
                   ^^^^^^^^^^^^^^^^^
E               IndexError: list index out of range

bowling.py:32: IndexError
_ BowlingTest.test_the_second_bonus_rolls_after_a_strike_in_the_last_frame_cannot_be_a_strike_if_the_first_one_is_not_a_strike _

self = <bowling_test.BowlingTest testMethod=test_the_second_bonus_rolls_after_a_strike_in_the_last_frame_cannot_be_a_strike_if_the_first_one_is_not_a_strike>

    def test_the_second_bonus_rolls_after_a_strike_in_the_last_frame_cannot_be_a_strike_if_the_first_one_is_not_a_strike(
        self,
    ):
        rolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 6]
>       game = self.roll_new_game(rolls)
               ^^^^^^^^^^^^^^^^^^^^^^^^^

bowling_test.py:145: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
bowling_test.py:16: in roll_new_game
    game.roll(roll)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <bowling.BowlingGame object at 0x105dd9730>, pins = 0

    def roll(self, pins):
        if not isinstance(pins, int) or pins < 0 or pins > 10:
            raise ValueError("pins must be an integer between 0 and 10")
    
        tenth_start = self._first_nine_end()
        if tenth_start is None:
            # A frame among the first nine is in progress.
            if self.rolls and self.rolls[-1] != 10:
                frame_start = len(self.rolls) - 1
                # Locate the start of the current frame by parsing completed frames.
                index = 0
                while index < frame_start:
                    index += 1 if self.rolls[index] == 10 else 2
>               if self.rolls[index] + pins > 10:
                   ^^^^^^^^^^^^^^^^^
E               IndexError: list index out of range

bowling.py:32: IndexError
_ BowlingTest.test_two_bonus_rolls_after_a_strike_in_the_last_frame_can_score_more_than_10_points_if_one_is_a_strike _

self = <bowling_test.BowlingTest testMethod=test_two_bonus_rolls_after_a_strike_in_the_last_frame_can_score_more_than_10_points_if_one_is_a_strike>

    def test_two_bonus_rolls_after_a_strike_in_the_last_frame_can_score_more_than_10_points_if_one_is_a_strike(
        self,
    ):
        rolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 10, 6]
>       game = self.roll_new_game(rolls)
               ^^^^^^^^^^^^^^^^^^^^^^^^^

bowling_test.py:138: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
bowling_test.py:16: in roll_new_game
    game.roll(roll)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <bowling.BowlingGame object at 0x105df5860>, pins = 0

    def roll(self, pins):
        if not isinstance(pins, int) or pins < 0 or pins > 10:
            raise ValueError("pins must be an integer between 0 and 10")
    
        tenth_start = self._first_nine_end()
        if tenth_start is None:
            # A frame among the first nine is in progress.
            if self.rolls and self.rolls[-1] != 10:
                frame_start = len(self.rolls) - 1
                # Locate the start of the current frame by parsing completed frames.
                index = 0
                while index < frame_start:
                    index += 1 if self.rolls[index] == 10 else 2
>               if self.rolls[index] + pins > 10:
                   ^^^^^^^^^^^^^^^^^
E               IndexError: list index out of range

bowling.py:32: IndexError
_ BowlingTest.test_two_bonus_rolls_after_a_strike_in_the_last_frame_cannot_score_more_than_10_points _

self = <bowling_test.BowlingTest testMethod=test_two_bonus_rolls_after_a_strike_in_the_last_frame_cannot_score_more_than_10_points>

    def test_two_bonus_rolls_after_a_strike_in_the_last_frame_cannot_score_more_than_10_points(
        self,
    ):
        rolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 5]
>       game = self.roll_new_game(rolls)
               ^^^^^^^^^^^^^^^^^^^^^^^^^

bowling_test.py:130: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
bowling_test.py:16: in roll_new_game
    game.roll(roll)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <bowling.BowlingGame object at 0x105df5b80>, pins = 0

    def roll(self, pins):
        if not isinstance(pins, int) or pins < 0 or pins > 10:
            raise ValueError("pins must be an integer between 0 and 10")
    
        tenth_start = self._first_nine_end()
        if tenth_start is None:
            # A frame among the first nine is in progress.
            if self.rolls and self.rolls[-1] != 10:
                frame_start = len(self.rolls) - 1
                # Locate the start of the current frame by parsing completed frames.
                index = 0
                while index < frame_start:
                    index += 1 if self.rolls[index] == 10 else 2
>               if self.rolls[index] + pins > 10:
                   ^^^^^^^^^^^^^^^^^
E               IndexError: list index out of range

bowling.py:32: IndexError
=========================== short test summary info ============================
FAILED bowling_test.py::BowlingTest::test_a_spare_followed_by_zeros_is_worth_ten_points
FAILED bowling_test.py::BowlingTest::test_a_spare_in_the_last_frame_gets_a_one_roll_bonus_that_is_counted_once
FAILED bowling_test.py::BowlingTest::test_a_strike_earns_ten_points_in_a_frame_with_a_single_roll
FAILED bowling_test.py::BowlingTest::test_a_strike_in_the_last_frame_gets_a_two_roll_bonus_that_is_counted_once
FAILED bowling_test.py::BowlingTest::test_a_strike_with_the_one_roll_bonus_after_a_spare_in_the_last_frame_does_not_get_a_bonus
FAILED bowling_test.py::BowlingTest::test_bonus_roll_after_a_strike_in_the_last_frame_cannot_score_more_than_10_points
FAILED bowling_test.py::BowlingTest::test_bonus_roll_for_a_spare_in_the_last_frame_must_be_rolled_before_score_can_be_calculated
FAILED bowling_test.py::BowlingTest::test_bonus_rolls_for_a_strike_in_the_last_frame_must_be_rolled_before_score_can_be_calculated
FAILED bowling_test.py::BowlingTest::test_both_bonus_rolls_for_a_strike_in_the_last_frame_must_be_rolled_before_score_can_be_calculated
FAILED bowling_test.py::BowlingTest::test_cannot_roll_after_bonus_roll_for_spare
FAILED bowling_test.py::BowlingTest::test_cannot_roll_after_bonus_rolls_for_strike
FAILED bowling_test.py::BowlingTest::test_cannot_roll_if_game_already_has_ten_frames
FAILED bowling_test.py::BowlingTest::test_consecutive_spares_each_get_a_one_roll_bonus
FAILED bowling_test.py::BowlingTest::test_consecutive_strikes_each_get_the_two_roll_bonus
FAILED bowling_test.py::BowlingTest::test_last_two_strikes_followed_by_only_last_bonus_with_non_strike_points
FAILED bowling_test.py::BowlingTest::test_points_scored_in_the_roll_after_a_spare_are_counted_twice
FAILED bowling_test.py::BowlingTest::test_points_scored_in_the_two_rolls_after_a_strike_are_counted_twice_as_a_bonus
FAILED bowling_test.py::BowlingTest::test_rolling_a_spare_with_the_two_roll_bonus_does_not_get_a_bonus_roll
FAILED bowling_test.py::BowlingTest::test_second_bonus_roll_after_a_strike_in_the_last_frame_cannot_score_more_than_10_points
FAILED bowling_test.py::BowlingTest::test_should_be_able_to_score_a_game_with_all_zeros
FAILED bowling_test.py::BowlingTest::test_should_be_able_to_score_a_game_with_no_strikes_or_spares
FAILED bowling_test.py::BowlingTest::test_strikes_with_the_two_roll_bonus_do_not_get_bonus_rolls
FAILED bowling_test.py::BowlingTest::test_the_second_bonus_rolls_after_a_strike_in_the_last_frame_cannot_be_a_strike_if_the_first_one_is_not_a_strike
FAILED bowling_test.py::BowlingTest::test_two_bonus_rolls_after_a_strike_in_the_last_frame_can_score_more_than_10_points_if_one_is_a_strike
FAILED bowling_test.py::BowlingTest::test_two_bonus_rolls_after_a_strike_in_the_last_frame_cannot_score_more_than_10_points
25 failed, 6 passed in 0.15s


Command exited with code 1
```

</details>

**Reply:**

→ tool `bash`

```
{
 "command": "python3 - <<'PY'\nfrom bowling import BowlingGame\nx=BowlingGame()\nfor n in range(25):\n try:\n  print(n, x.rolls, x._first_nine_end())\n  x.roll(0)\n except Exception as e:\n  print('error',n,type(e),e);break\nPY"
}
```

## Call 8 · main agent

35,567 in (34,712 cached) · 907 out · $0.0009 · 9526 ms · OpenRouter id `gen-1793672245-S8cM2pPXNDlmI4koI16G`

**New in this request** (continues call 7):

**assistant → tool `bash`**

```
{
 "command": "python3 - <<'PY'\nfrom bowling import BowlingGame\nx=BowlingGame()\nfor n in range(25):\n try:\n  print(n, x.rolls, x._first_nine_end())\n  x.roll(0)\n except Exception as e:\n  print('error',n,type(e),e);break\nPY"
}
```

**tool result** (`call_4Ym8EfdILdu7su4WKti7YJ7V`)

```
0 [] None
1 [0] None
2 [0, 0] None
error 2 <class 'IndexError'> list index out of range

```

**Reply:**

*reasoning:* **Simplifying frame calculations**

I'm working on a way to simplify the roll path for calculating frames. If a roll equals 10, I can increase the index and frame count. Otherwise, I check if I'm at the end of my rolls to process them correctly. If not, I adjust the index and continue. Once the frame count reaches 9, I need to handle the tenth frame. I'll create a helper to determine if the frame is complete and possibly replace the current calculation method for clarity.

→ tool `edit`

```
{
 "path": "bowling.py",
 "edits": [
  {
   "oldText": "        if tenth_start is None:\n            # A frame among the first nine is in progress.\n            if self.rolls and self.rolls[-1] != 10:\n                frame_start = len(self.rolls) - 1\n                # Locate the start of the current frame by parsing completed frames.\n                index = 0\n                while index < frame_start:\n                    index += 1 if self.rolls[index] == 10 else 2\n                if self.rolls[index] + pins > 10:\n                    raise ValueError(\"a frame cannot knock down more than 10 pins\")",
   "newText": "        if tenth_start is None:\n            # Check whether the next roll is the second ball in a frame.\n            index = 0\n            frame = 0\n            while frame < 9 and index < len(self.rolls):\n                if self.rolls[index] == 10:\n                    index += 1\n                    frame += 1\n                elif index + 1 >= len(self.rolls):\n                    if self.rolls[index] + pins > 10:\n                        raise ValueError(\"a frame cannot knock down more than 10 pins\")\n                    break\n                else:\n                    index += 2\n                    frame += 1"
  }
 ]
}
```

## Call 9 · main agent

36,495 in (35,564 cached) · 63 out · $0.0005 · 1713 ms · OpenRouter id `gen-1793672255-3jwVzerQbMU61kk2zwHy`

**New in this request** (continues call 8):

**assistant → tool `edit`**

```
{
 "path": "bowling.py",
 "edits": [
  {
   "oldText": "        if tenth_start is None:\n            # A frame among the first nine is in progress.\n            if self.rolls and self.rolls[-1] != 10:\n                frame_start = len(self.rolls) - 1\n                # Locate the start of the current frame by parsing completed frames.\n                index = 0\n                while index < frame_start:\n                    index += 1 if self.rolls[index] == 10 else 2\n                if self.rolls[index] + pins > 10:\n                    raise ValueError(\"a frame cannot knock down more than 10 pins\")",
   "newText": "        if tenth_start is None:\n            # Check whether the next roll is the second ball in a frame.\n            index = 0\n            frame = 0\n            while frame < 9 and index < len(self.rolls):\n                if self.rolls[index] == 10:\n                    index += 1\n                    frame += 1\n                elif index + 1 >= len(self.rolls):\n                    if self.rolls[index] + pins > 10:\n                        raise ValueError(\"a frame cannot knock down more than 10 pins\")\n                    break\n                else:\n                    index += 2\n                    frame += 1"
  }
 ]
}
```

**tool result** (`call_DZl7ntf6ZazsiEUBlbYtadhU`)

```
Successfully replaced 1 block(s) in bowling.py.
```

**Reply:**

→ tool `bash`

```
{
 "command": "python3 -m pytest -q",
 "timeout": 120000
}
```

## Call 10 · main agent

37,502 in (36,492 cached) · 293 out · $0.0006 · 3717 ms · OpenRouter id `gen-1793672256-DDAa6fKONblsIjYMMreD`

**New in this request** (continues call 9):

**assistant → tool `bash`**

```
{
 "command": "python3 -m pytest -q",
 "timeout": 120000
}
```

**tool result** (`call_OS2WpmPPFmWRQVfoxqxX9fgY`)

<details><summary>77 lines</summary>

```
..F..F.........................                                          [100%]
=================================== FAILURES ===================================
_ BowlingTest.test_a_spare_in_the_last_frame_gets_a_one_roll_bonus_that_is_counted_once _

self = <bowling_test.BowlingTest testMethod=test_a_spare_in_the_last_frame_gets_a_one_roll_bonus_that_is_counted_once>

    def test_a_spare_in_the_last_frame_gets_a_one_roll_bonus_that_is_counted_once(self):
        rolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 3, 7]
        game = self.roll_new_game(rolls)
>       self.assertEqual(game.score(), 17)
                         ^^^^^^^^^^^^

bowling_test.py:47: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <bowling.BowlingGame object at 0x1088f5310>

    def score(self):
        tenth_start = self._first_nine_end()
        if tenth_start is None:
            raise ValueError("cannot score an incomplete game")
    
        tenth = self.rolls[tenth_start:]
        if not tenth:
            raise ValueError("cannot score an incomplete game")
        if tenth[0] == 10:
            if len(tenth) != 3:
                raise ValueError("strike fill balls are incomplete")
        elif len(tenth) == 2 and sum(tenth) == 10:
            raise ValueError("spare fill ball is missing")
        elif len(tenth) != 2:
>           raise ValueError("cannot score an incomplete game")
E           ValueError: cannot score an incomplete game

bowling.py:73: ValueError
_ BowlingTest.test_a_strike_with_the_one_roll_bonus_after_a_spare_in_the_last_frame_does_not_get_a_bonus _

self = <bowling_test.BowlingTest testMethod=test_a_strike_with_the_one_roll_bonus_after_a_spare_in_the_last_frame_does_not_get_a_bonus>

    def test_a_strike_with_the_one_roll_bonus_after_a_spare_in_the_last_frame_does_not_get_a_bonus(
        self,
    ):
        rolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 3, 10]
        game = self.roll_new_game(rolls)
>       self.assertEqual(game.score(), 20)
                         ^^^^^^^^^^^^

bowling_test.py:93: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <bowling.BowlingGame object at 0x108a08b90>

    def score(self):
        tenth_start = self._first_nine_end()
        if tenth_start is None:
            raise ValueError("cannot score an incomplete game")
    
        tenth = self.rolls[tenth_start:]
        if not tenth:
            raise ValueError("cannot score an incomplete game")
        if tenth[0] == 10:
            if len(tenth) != 3:
                raise ValueError("strike fill balls are incomplete")
        elif len(tenth) == 2 and sum(tenth) == 10:
            raise ValueError("spare fill ball is missing")
        elif len(tenth) != 2:
>           raise ValueError("cannot score an incomplete game")
E           ValueError: cannot score an incomplete game

bowling.py:73: ValueError
=========================== short test summary info ============================
FAILED bowling_test.py::BowlingTest::test_a_spare_in_the_last_frame_gets_a_one_roll_bonus_that_is_counted_once
FAILED bowling_test.py::BowlingTest::test_a_strike_with_the_one_roll_bonus_after_a_spare_in_the_last_frame_does_not_get_a_bonus
2 failed, 29 passed in 0.02s


Command exited with code 1
```

</details>

**Reply:**

*reasoning:* **Revising scoring logic**

I'm working on a scoring system that needs validation for spares and strikes. If the length is 2, I need to return an error, and if it's not equal to 2, it should reject it if the length isn't 3. I also have to add a frame validity check for the first strike. So, if the first strike has a length of 3, that’s good. Otherwise, if the sum of the first two is 10, it requires a length of 3 for validity.

→ tool `edit`

```
{
 "path": "bowling.py",
 "edits": [
  {
   "oldText": "        if tenth[0] == 10:\n            if len(tenth) != 3:\n                raise ValueError(\"strike fill balls are incomplete\")\n        elif len(tenth) == 2 and sum(tenth) == 10:\n            raise ValueError(\"spare fill ball is missing\")\n        elif len(tenth) != 2:\n            raise ValueError(\"cannot score an incomplete game\")",
   "newText": "        if tenth[0] == 10:\n            if len(tenth) != 3:\n                raise ValueError(\"strike fill balls are incomplete\")\n        elif len(tenth) >= 2 and sum(tenth[:2]) == 10:\n            if len(tenth) != 3:\n                raise ValueError(\"spare fill ball is missing\")\n        elif len(tenth) != 2:\n            raise ValueError(\"cannot score an incomplete game\")"
  }
 ]
}
```

## Call 11 · main agent

37,816 in (37,499 cached) · 29 out · $0.0004 · 1282 ms · OpenRouter id `gen-1793672260-3jIuthoGGylBfi3o6rNk`

**New in this request** (continues call 10):

**assistant → tool `edit`**

```
{
 "path": "bowling.py",
 "edits": [
  {
   "oldText": "        if tenth[0] == 10:\n            if len(tenth) != 3:\n                raise ValueError(\"strike fill balls are incomplete\")\n        elif len(tenth) == 2 and sum(tenth) == 10:\n            raise ValueError(\"spare fill ball is missing\")\n        elif len(tenth) != 2:\n            raise ValueError(\"cannot score an incomplete game\")",
   "newText": "        if tenth[0] == 10:\n            if len(tenth) != 3:\n                raise ValueError(\"strike fill balls are incomplete\")\n        elif len(tenth) >= 2 and sum(tenth[:2]) == 10:\n            if len(tenth) != 3:\n                raise ValueError(\"spare fill ball is missing\")\n        elif len(tenth) != 2:\n            raise ValueError(\"cannot score an incomplete game\")"
  }
 ]
}
```

**tool result** (`call_qY8ma8Sxownk0RA1TP8FEu7f`)

```
Successfully replaced 1 block(s) in bowling.py.
```

**Reply:**

→ tool `bash`

```
{
 "command": "python3 -m pytest -q",
 "timeout": 120000
}
```

## Call 12 · main agent

37,872 in (37,813 cached) · 35 out · $0.0004 · 1347 ms · OpenRouter id `gen-1793672262-cfivnhC9S2ooIICrv8du`

**New in this request** (continues call 11):

**assistant → tool `bash`**

```
{
 "command": "python3 -m pytest -q",
 "timeout": 120000
}
```

**tool result** (`call_KOCCFuw2eVAc0TaRLG7VJYr4`)

```
...............................                                          [100%]
31 passed in 0.01s

```

**Reply:**

```
Implemented bowling scoring and roll validation in `bowling.py`, including strike/spare bonuses and tenth-frame fill balls. All tests pass: `31 passed`.
```

