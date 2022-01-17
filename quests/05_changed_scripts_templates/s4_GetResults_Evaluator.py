"""
This script was created at 09-Dec-21
author: eachrist

"""
"""

    def calculate_metrics(self, original_user: str, sets_dict: dict):

        # Evaluate its module
        for idx, data_type in enumerate(['acc', 'gyr', 'swp', 'tap']):
            trn = sets_dict['trn'][idx][['Decision', 'Prediction']]
            tst = sets_dict['tst'][idx][['Decision', 'Prediction']]
            att = sets_dict['att'][idx][['User', 'Decision', 'Prediction']]
            self.OriginalUser.append(original_user)
            self.Module.append(data_type)
            self.NumOfTrnData.append(len(trn))
            self.NumOfTstData.append(len(tst))
            self.NumOfAttData.append(att.shape[0])
            self.NumOfAtt.append(len(set(att['User'])))
            FRR, NumOfUnlocks, FRRConf = evaluate_original_user(trn, self.screen)
            self.FRR_trn.append(FRR)
            self.FRRConf_trn.append(FRRConf)
            self.NumOfUnlocks_trn.append(NumOfUnlocks)
            FRR, NumOfUnlocks, FRRConf = evaluate_original_user(tst, self.screen)
            self.FRR_tst.append(FRR)
            self.FRRConf_tst.append(FRRConf)
            self.NumOfUnlocks_tst.append(NumOfUnlocks)
            FAR, NumOfAcceptTL = evaluate_attackers(att, self.screen)
            self.FAR.append(FAR)
            self.NumOfAcceptTL.append(NumOfAcceptTL)

        return

"""
