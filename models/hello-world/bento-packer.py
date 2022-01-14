from serving import SudokuRating
from joblib import load

sudoku_rating_service = SudokuRating()

model = load("linearregression.joblib")

sudoku_rating_service.pack('linearregression', model)

# Save the prediction service to disk for model serving
saved_path = sudoku_rating_service.save()