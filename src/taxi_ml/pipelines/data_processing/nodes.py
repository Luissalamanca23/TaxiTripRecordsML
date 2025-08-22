"""
Data processing nodes for NYC Taxi ML project.
"""

import pandas as pd
import logging
from typing import Tuple, Dict

logger = logging.getLogger(__name__)


def preprocess_taxi_data(raw_data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Clean and preprocess the NYC taxi dataset.
    
    Args:
        raw_data: Dictionary of raw taxi trip data partitions
        
    Returns:
        Cleaned and preprocessed data
    """
    logger.info("Starting taxi data preprocessing")
    
    # Concatenate all partitioned datasets
    data_frames = []
    for partition_id, partition_data in raw_data.items():
        data_frames.append(partition_data)
    
    data = pd.concat(data_frames, ignore_index=True)
    
    # Basic info about the dataset
    logger.info(f"Combined dataset shape: {data.shape}")
    logger.info(f"Columns: {list(data.columns)}")
    
    # Data cleaning for taxi trips
    # Remove invalid trips (negative amounts, zero distance, etc.)
    data = data[data['total_amount'] > 0]
    data = data[data['fare_amount'] > 0]
    data = data[data['trip_distance'] > 0]
    
    # Remove outliers (trips longer than 100 miles or more than $500)
    data = data[data['trip_distance'] <= 100]
    data = data[data['total_amount'] <= 500]
    
    # Calculate trip duration
    data['trip_duration'] = (data['tpep_dropoff_datetime'] - data['tpep_pickup_datetime']).dt.total_seconds() / 60
    
    # Remove trips with invalid duration (negative or more than 8 hours)
    data = data[(data['trip_duration'] > 0) & (data['trip_duration'] <= 480)]
    
    # Extract time features
    data['pickup_hour'] = data['tpep_pickup_datetime'].dt.hour
    data['pickup_day'] = data['tpep_pickup_datetime'].dt.dayofweek
    data['pickup_month'] = data['tpep_pickup_datetime'].dt.month
    
    # Handle missing values
    missing_values = data.isnull().sum()
    if missing_values.sum() > 0:
        logger.warning(f"Found missing values: {missing_values[missing_values > 0]}")
        data = data.dropna()
    
    # Convert categorical variables
    categorical_cols = ['VendorID', 'RatecodeID', 'store_and_fwd_flag', 
                       'PULocationID', 'DOLocationID', 'payment_type']
    
    for col in categorical_cols:
        if col in data.columns:
            data[col] = data[col].astype('category')
    
    logger.info(f"Processed dataset shape: {data.shape}")
    return data


def split_data(data: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Split data into train, validation, and test sets.
    
    Args:
        data: Preprocessed data
        
    Returns:
        Tuple of (train_data, val_data, test_data)
    """
    from sklearn.model_selection import train_test_split
    
    logger.info("Splitting data into train/val/test sets")
    
    # First split: train+val vs test (80% vs 20%)
    train_val, test = train_test_split(data, test_size=0.2, random_state=42)
    
    # Second split: train vs val (80% vs 20% of train_val, which gives us 64%/16%/20% split)
    train, val = train_test_split(train_val, test_size=0.2, random_state=42)
    
    logger.info(f"Train set: {len(train)} samples")
    logger.info(f"Validation set: {len(val)} samples") 
    logger.info(f"Test set: {len(test)} samples")
    
    return train, val, test
