from calc.calculate_phase_base import CalculatePhaseBase
from model.reward_log import RewardLog, TYPE_FOUNDERS_PARENT, TYPE_OWNERS_PARENT, TYPE_FOUNDER, TYPE_OWNER
from util.rounding_command import RoundingCommand

MUTEZ = 1e+6


class CalculatePhase4(CalculatePhaseBase):
    """
    At stage 4, Founders_parent and owners_parent records are split into founder and owner records.

    If there are 2 owner definition in owners_map, owners_parent record from phase3 will have two phase4 children.
    Sum of owner ratios equals to ratio of owners_parent record.
    """

    def __init__(self, founders_map, owners_map, prcnt_rm=RoundingCommand(None)) -> None:
        super().__init__()

        self.founders_map = founders_map
        self.owners_map = owners_map
        self.prcnt_rm = prcnt_rm

    def calculate(self, reward_data3, total_amount):

        rewards = []

        for rl3 in self.iterateskipped(reward_data3):
            # move skipped records to next phase
            rewards.append(rl3)

        for rl3 in self.filterskipped(reward_data3):
            if rl3.type == TYPE_FOUNDERS_PARENT:
                for addr, ratio in self.founders_map.items():
                    rl4 = RewardLog(addr, TYPE_FOUNDER, 0)
                    # new ratio is parent ratio * ratio of the founder
                    rl4.ratio4 = self.prcnt_rm.round(ratio * rl3.ratio3)
                    rewards.append(rl4)

            elif rl3.type == TYPE_OWNERS_PARENT:
                for addr, ratio in self.owners_map.items():
                    rl4 = RewardLog(addr, TYPE_OWNER, 0)
                    # new ratio is parent ratio * ratio of the owner
                    rl4.ratio4 = self.prcnt_rm.round(ratio * rl3.ratio3)
                    rewards.append(rl4)
            else:
                rl3.ratio4 = rl3.ratio3
                rewards.append(rl3)

        return rewards, total_amount