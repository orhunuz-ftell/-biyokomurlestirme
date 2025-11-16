import os
import glob
import pandas as pd
from randomforest import BiooilPredictor

if __name__ == "__main__":
    data_dir = r'C:\@biyokomurlestirme\python_codes\BiooilAI\ProcessedData'
    predictor = BiooilPredictor()

    # processed_data_{target}_X_train.csv dosyalarını bul
    pattern = os.path.join(data_dir, 'processed_data_*_X_train.csv')
    for train_path in glob.glob(pattern):
        fname = os.path.basename(train_path)
        # 'processed_data_acids_X_train.csv' -> target='acids'
        target = fname.split('_')[2]

        # Dosya yollarını oluştur
        X_train = pd.read_csv(train_path)
        X_test  = pd.read_csv(os.path.join(
            data_dir, f'processed_data_{target}_X_test.csv'))
        y_train = pd.read_csv(os.path.join(
            data_dir, f'processed_data_{target}_y_train.csv'))
        y_test  = pd.read_csv(os.path.join(
            data_dir, f'processed_data_{target}_y_test.csv'))

        print(f"\n>> '{target}' için eğitim başlıyor")
        predictor.train_models(X_train, X_test, y_train, y_test)

    predictor.print_r2_scores()

    # Modelleri kaydet
    out_dir = os.path.join(data_dir, 'rf_models')
    os.makedirs(out_dir, exist_ok=True)
    predictor.save_models(path=os.path.join(out_dir, 'rf_model'))

    print("\nTüm hedefler için eğitim tamamlandı.")
