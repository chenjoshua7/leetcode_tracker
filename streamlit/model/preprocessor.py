from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd

class PreprocessData(BaseEstimator, TransformerMixin):
    def __init__(self) -> None:
        self.skills = None
        self.fitted = False
        self.columns_ = None
        
    def fit(self, df, y=None):
        self.skills = df['skills'].str.split(',').explode().str.strip().unique()
        self.fitted = True
        return self
    
    def transform(self, df):
        columns = ["complexity", "acceptance_rate", "skills"]
        
        if not self.fitted:
            raise AssertionError("Model has not been fit")
        df = df.copy()
        df = df[columns]
        df = self._ohe_complexity(df)
        df = self._ohe_skills(df)
        df = df.drop(["complexity", "skills"], axis = 1)
        self.columns_ = df.columns
        return df 
    
    def _ohe_complexity(self, df) -> pd.DataFrame:
        complexity = ["Easy", "Medium", "Hard"]
        
        for level in complexity:
            df[f'complexity_{level}'] = df['complexity'].apply(lambda x: 1 if x == level else 0)
        
        return df
    
    def _ohe_skills(self, df) -> pd.DataFrame:
        for skill in self.skills:
            df[f'skill_{skill}'] = df['skills'].apply(lambda x: 1 if skill in x.split(',') else 0)
        
        return df