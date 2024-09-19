from celery import shared_task
import pandas as pd
import os

@shared_task
def process_csv_task(file_path, operation, column=None, filters=None):
    output_file_path = None
    try:
        # Read the CSV file
        print("reading file")
        df = pd.read_csv(file_path)
        
        print("df", df)

        # Drop completely empty rows
        df.dropna(how='all', inplace=True)
        print(f"Available columns: {df.columns.tolist()}")

        if operation == "dedup":
            # Remove duplicate rows based on all columns
            df = df.drop_duplicates()


        elif operation == "unique":
            if column is None:
                return {'error': 'Column name is required for unique operation'}
            if column in df.columns:
                # Extract unique values from the specified column
                unique_values = df[column].drop_duplicates().reset_index(drop=True)

                # Create a DataFrame for unique values
                unique_df = pd.DataFrame(unique_values, columns=[column])

                # Save the unique values to a new CSV file
                output_file_name = f"unique_{os.path.basename(file_path)}"
                output_file_path = os.path.join(os.path.dirname(file_path), output_file_name)
                unique_df.to_csv(output_file_path, index=False)

                return {
                    'data': unique_values.tolist(),
                    'file_link': output_file_path
                }
            else:
                return {'error': f'Column {column} not found in CSV'}

        elif operation == "filter":
            if filters is None:
                return {'error': 'Filtering conditions are required for filter operation'}
            try:
                # Apply filtering conditions
                for key, value in filters.items():
                    if key in df.columns:
                        df = df[df[key] == value]
                    else:
                        return {'error': f'Column {key} not found in CSV'}

                # Save the filtered data to a new CSV file
                output_file_name = f"filtered_{os.path.basename(file_path)}"
                output_file_path = os.path.join(os.path.dirname(file_path), output_file_name)
                df.to_csv(output_file_path, index=False)

                return {
                    'data': df.head(100).to_dict('records'),  # Return first 100 rows as dict
                    'file_link': output_file_path
                }
            except Exception as e:
                return {'error': f'Error applying filters: {str(e)}'}

        else:
            return {'error': 'Invalid operation'}

    except Exception as e:
        # Log the error
        error_message = f"Error processing CSV: {str(e)}"
        print(error_message)
        # Return error information
        return {
            'error': error_message,
            'file_path': file_path,
            'operation': operation,
            'column': column,
            'filters': filters,
            'output_file_path': output_file_path
        }

