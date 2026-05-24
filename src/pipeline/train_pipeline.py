from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer


if __name__ == "__main__":
    # Stage 1: Ingest
    obj = DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion()

    # Stage 2: Transform
    data_transformation = DataTransformation()
    train_arr, test_arr, _ = data_transformation.initiate_data_transformation(train_data, test_data)

    # Stage 3: Train
    model_trainer = ModelTrainer()
    r2 = model_trainer.initiate_model_trainer(train_arr, test_arr)
    print(f"Best model R² score: {r2}")
