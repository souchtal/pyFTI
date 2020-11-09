from enum import Enum


class FTIT_level(Enum):
	FTI_L1 = 1,
    FTI_L2,
    FTI_L3,
    FTI_L4,
    FTI_L1_DCP,
    FTI_L2_DCP,
    FTI_L3_DCP,
    FTI_L4_DCP,
    FTI_L4_H5_SINGLE,
    FTI_MIN_LEVEL_ID = FTI_L1,
    FTI_MAX_LEVEL_ID = FTI_L4_H5_SINGLE

