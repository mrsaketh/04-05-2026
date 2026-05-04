'''Write a python program, that will analyze a given csv ,
 
1.decide what columns are present and
 
2figure out what statistical analayis method is most applicable and
 
3.apply that mechanism'''
 
import pandas as pd
import os
import numpy as np
 
import matplotlib.pyplot as plt
 
from scipy import stats

#step1:- Take CSV file as input
file_path=input("enter csv filename:").strip()
def load_data():
 
    try:
 
        df=pd.read_csv(file_path)
 
        print("\n Csv Loaded successfully")
 
        return df
 
    except FileNotFoundError:
 
        print("\nFile not found.")
 
df=load_data()

def clean_column_name(name):
    """
    Clean column names for filenames.
    """
    return str(name).replace(" ", "_").replace("/", "_").replace("\\", "_")

def show_dataset(df):
 
    print("Dataset Preview")
 
    print(df)
 
    print("Column Information")
 
    print(df.dtypes)
 
show_dataset(df)
 

#step2: clean the dataset
 
def clean_data(df):
 
    return df.dropna()
 
clean_data(df)
 
#step3. Differentiate the columns categorical and non categorical
def categorize_columns(df):
 
    num_cols=[]
    date_cols=[]
    boolean_cols=[]
    cat_cols=[]
    text_cols=[]
    id_cols=[]
    location_cols=[]
    
    for col in df.columns:

        
        if df[col].dtype=='object':
            cat_cols.append(col)
 
        elif df[col].dtype=='date':
            date_cols.append(col)
        elif df[col].dtype=='bool':
            boolean_cols.append(col)
        elif df[col].dtype=='int64':
            num_cols.append(col)
        elif df[col].dtype=='int64':
            id_cols.append(col)
        elif df[col].dtype=='object':
            location_cols.append(col)
        else:
            return "Invalid type "
      
            
 
    return num_cols,cat_cols,date_cols,boolean_cols,text_cols,id_cols,location_cols
num_cols,cat_cols,date_cols,boolean_cols,text_cols,id_cols,location_cols = categorize_columns(df)
 
#step 4: Decide what column requires what type of analysis
 
def numeric_cols(df,num_cols):
 
    for column in num_cols:
        print("\nColumn:", column)
        print("Minimum:", df[column].min())
        print("Maximum:", df[column].max())
        print("Mean:", df[column].mean())
        print("Median:", df[column].median())
 
        print("Range:", (df[column].max()-df[column].min()))
 
        print("Standard Deviation:", df[column].std())
 
        print("Variance:", df[column].var())
 
        print("Sum:", df[column].sum())
 
        print("Z_score:" ,stats.zscore(df[column]))
 
        print("Quartile 1 :" ,df[column].quantile(0.25))
 
        print("Quartile 2 :" ,df[column].quantile(0.50))
 
        print("Quartile 3 :" ,df[column].quantile(0.75))
 
        print("IQR :" ,df[column].quantile(0.75)-df[column].quantile(0.25))
 
 

#step5: Perform the statistical methods as decided in step4 for the columns
def categorical_cols(df , cat_cols):
 
    for column in cat_cols:
        print("\nColumn:", column)
        print("Unique values:", df[column].nunique())
        print("Most common value:")
 
        mode_value = df[column].mode()
 
        if not mode_value.empty:
            print(mode_value[0])
        else:
            print("No mode found")
 
        print("\nTop 5 most frequent values:")
        print(df[column].value_counts().head())

 
categorical_cols(df,cat_cols)
def chi_square(df):
 
    col1=input("enter column 1")
 
    col2=input("enter column 2")
 
    if col1 in cat_cols and col2 in cat_cols:
 
        contingency_table = pd.crosstab(df[col1], df[col2])
 
        print(contingency_table)
 
        chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
 
        print("\nExpected Frequency Table:")
        expected_df = pd.DataFrame(
            expected,
            index=contingency_table.index,
            columns=contingency_table.columns
        )
 
        print(expected_df)
 
        print("\nChi-Square Result:")
        print("Chi-square statistic:", chi2)
        print("Degrees of freedom:", dof)
        print("p-value:", p_value)
 
        print("\nInterpretation:")
        if p_value < 0.05:
            print("p-value < 0.05, so the two categorical variables are likely associated.")
        else:
            print("p-value >= 0.05, so there is no strong evidence of association.")
 
    else:
 
        print("It is only applicable for categorical columns")
 
 
 
#CORRELATION
 
def correlation(df,num_cols):
    col1=input("Enter first column")
    col2 =input("Enter Second column")
 
    x= df[col1]
    y= df[col2]
 
    correlation =x.corr(y)
    print(f"\nCol1: {col1}")
    print(f"Col2: {col2}")
    print("Correlation:", correlation)
    print("\nInterpretation:")
    if correlation > 0.7:
        print("Strong positive relationship.")
    elif correlation > 0.3:
        print("Moderate positive relationship.")
    elif correlation > 0:
        print("Weak positive relationship.")
    elif correlation < -0.7:
        print("Strong negative relationship.")
    elif correlation < -0.3:
        print("Moderate negative relationship.")
    elif correlation < 0:
        print("Weak negative relationship.")
    else:
        print("No relationship.")
 
 
 
#SIMPLE LINEAR REGRESSION
 
 
def linear_regression_demo(df):
 
    col1=input("Enter first column")
    col2 =input("Enter Second column")
 
    x= df[col1]
    y= df[col2]
 
    result = stats.linregress(x,y)
 
    print(f"\nIndependent Variable X: {col1}")
    print(f"Dependent Variable Y: {col2}")
    print("\nRegression Results:")
    print("Slope m:", result.slope)
    print("Intercept c:", result.intercept)
    print("R-value:", result.rvalue)
    print("R-squared:", result.rvalue ** 2)
    print("P-value:", result.pvalue)
 
    
    print("\nFinal Equation:")
    print(f"{col2} = {result.slope:.4f} × {col1} + {result.intercept:.4f}")
    sample_x = 80
    predicted_y = result.slope * sample_x + result.intercept
    print(f"\nPrediction Example:")
    print(f"If {col1} = {sample_x}, predicted {col2} = {predicted_y:.2f}")
 
 
 
#One Sample t Test
 
def one_sample_t_test(df):
    col =input("Enter the required column")
    expected_mean = 75
 
    values =df[col]
 
    
    t_statistic, p_value = stats.ttest_1samp(values, expected_mean)
 
 
    print(f"\nColumn Used: {col}")
    print("Expected Mean:", expected_mean)
    print("Actual Sample Mean:", values.mean())
    print("\nt-statistic:", t_statistic)
    print("p-value:", p_value)
    print("\nInterpretation:")
    if p_value < 0.05:
        print("p-value < 0.05, so the sample mean is significantly different from the expected mean.")
    else:
        print("p-value >= 0.05, so there is no strong evidence of a significant difference.")
 
 
 
 
def independent_t_test(df):
    group_column ="gender"
 
    value_column ="reading score"
 
    group1 = df[df[group_column] == "male"][value_column]
    group2 = df[df[group_column] == "female"][value_column]
    t_statistic, p_value = stats.ttest_ind(group1, group2, equal_var=False)
    print(f"\nGroup Column: {group_column}")
    print(f"Value Column: {value_column}")
    print("\nMale Scores:", group1.tolist())
    print("Female Scores:", group2.tolist())
    print("\nMale Mean:", group1.mean())
    print("Female Mean:", group2.mean())
    print("\nt-statistic:", t_statistic)
    print("p-value:", p_value)
    print("\nInterpretation:")
    if p_value < 0.05:
        print("p-value < 0.05, so the two group means are significantly different.")
    else:
        print("p-value >= 0.05, so there is no strong evidence of a significant difference between groups.")
 
 
 
#ONE WAY ANOVA
 
 
def anova_demo(df):
    group_column = "parental level of education"
    value_column = "math score"
 
    groups = []
 
    print(f"\nGroup Column: {group_column}")
    print(f"Value Column: {value_column}")
 
    
    for group_name in df[group_column].unique():
        group_values = df[df[group_column] == group_name][value_column]
        groups.append(group_values)
        print(f"\nGroup: {group_name}")
        print("Values:", group_values.tolist())
        print("Mean:", group_values.mean())
    f_statistic, p_value = stats.f_oneway(*groups)
 
    print("\nANOVA Result:")
    print("F-statistic:", f_statistic)
    print("p-value:", p_value)
    print("\nInterpretation:")
    if p_value < 0.05:
        print("p-value < 0.05, so at least one group mean is significantly different.")
        print("Important: ANOVA tells that a difference exists, but not exactly which group differs.")
        print("For that, a post-hoc test such as Tukey HSD is normally used.")
    else:
        print("p-value >= 0.05, so there is no strong evidence of difference among group means.")
 
def menu():
    print("\nChoose a statistical method:")
    print("1. numerical Operations")
    print("2. Correlation")
    print("3. Simple Linear Regression")
    print("4. One Sample t-Test")
    print("5. Independent Two Sample t-Test")
    print("6. One-Way ANOVA")
    print("7. Chi-Square Test")
    print("8. Run All")
    print("0. Exit")
 
 
def run_all(df):
    numeric_cols(df,num_cols)
    correlation(df,num_cols)
    linear_regression_demo(df)
    one_sample_t_test(df)
    independent_t_test(df)
    anova_demo(df)
    chi_square(df)

def add_suggestion(suggestions, graph_type, reason, columns, priority):
    """
    Add graph suggestion with priority.
    Higher priority means stronger recommendation.
    """
    suggestions.append({
        "graph_type": graph_type,
        "reason": reason,
        "columns": columns,
        "priority": priority
    })

def suggest_graphs(df, num_cols,cat_cols,date_cols,boolean_cols,text_cols,id_cols,location_cols):
    """
    Suggest graphs intelligently based on dataset structure.
    """
    suggestions = []
    numeric = num_cols
    categorical = cat_cols
    datetime = date_cols
    boolean =boolean_cols
    text=text_cols
    ids = id_cols
    location = location_cols
    
    row_count = len(df)


     
    # 1. One numeric column: distribution analysis
    for num_col in numeric:
        valid_count = df[num_col].dropna().shape[0]
        if valid_count >= 5:
            add_suggestion(suggestions, "Histogram", "Best for understanding distribution of a numeric column.", [num_col], 96)
            add_suggestion(suggestions, "Box Plot", "Best for finding spread, median, and outliers.", [num_col], 75)

    # 2. Two numeric columns: relationship analysis
    if len(numeric) >= 2:
        for i in range(len(numeric)):
            for j in range(i + 1, len(numeric)):
                add_suggestion(suggestions, "Scatter Plot", "Best for checking relationship between two numeric columns.", [numeric[i], numeric[j]], 90)

    # 3. Multiple numeric columns: line comparison
    if len(numeric) >= 2 and row_count <= 5000:
        add_suggestion(suggestions, "Multi-Line Plot", "Useful for comparing multiple numeric columns across row order.", numeric[:5], 60)

    # 4. Date + numeric: time trend
    if len(datetime) >= 1 and len(numeric) >= 1:
        for date_col in datetime:
            for num_col in numeric:
                add_suggestion(suggestions, "Time Series Line Chart", "Best for showing how a numeric value changes over time.", [date_col, num_col], 100)

    # 5. Categorical count chart
    for cat_col in categorical:
        unique_count = df[cat_col].nunique(dropna=True)
        if 2 <= unique_count <= 20:
            add_suggestion(suggestions, "Bar Chart", "Best for showing count/frequency of categories.", [cat_col], 20)
        if 2 <= unique_count <= 6:
            add_suggestion(suggestions, "Pie Chart", "Useful only when there are very few categories.", [cat_col], 90)

    # 6. Category + numeric: comparison across groups
    if len(categorical) >= 1 and len(numeric) >= 1:
        for cat_col in categorical:
            unique_count = df[cat_col].nunique(dropna=True)
            if 2 <= unique_count <= 20:
                for num_col in numeric:
                    add_suggestion(suggestions, "Category vs Numeric Bar Chart", "Best for comparing average numeric values across categories.", [cat_col, num_col], 20)
                    add_suggestion(suggestions, "Grouped Box Plot", "Best for comparing numeric spread across categories.", [cat_col, num_col], 88)
    # 7. Boolean columns
    for bool_col in boolean:
        add_suggestion(suggestions, "Boolean Bar Chart", "Best for showing True/False counts.", [bool_col], 70)

    
    # 8. Numeric correlation
    if len(numeric) >= 3:
        add_suggestion(suggestions, "Correlation Matrix", "Best for understanding relationships among multiple numeric columns.", numeric, 92)

    return sorted(suggestions, key=lambda x: x["priority"], reverse=True)
def plot_histogram(df, columns, output_folder):
    col = columns[0]
    plt.figure(figsize=(8, 5))
    plt.hist(df[col].dropna(), bins=20, edgecolor="black")
    plt.title(f"Histogram of {col}")
    plt.xlabel(col)
    plt.ylabel("Frequency")
    plt.grid(True)
    save_or_show_plot(output_folder, f"histogram_{clean_column_name(col)}.png")

def plot_boxplot(df, columns, output_folder):
    col = columns[0]
    plt.figure(figsize=(8, 5))
    plt.boxplot(df[col].dropna())
    plt.title(f"Box Plot of {col}")
    plt.ylabel(col)
    plt.grid(True)
    save_or_show_plot(output_folder, f"boxplot_{clean_column_name(col)}.png")

def plot_scatter(df, columns, output_folder):
    x_col, y_col = columns[0], columns[1]
    plt.figure(figsize=(8, 5))
    plt.scatter(df[x_col], df[y_col])
    plt.title(f"Scatter Plot: {x_col} vs {y_col}")
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.grid(True)
    save_or_show_plot(output_folder, f"scatter_{clean_column_name(x_col)}_vs_{clean_column_name(y_col)}.png")

def plot_time_series(df, columns, output_folder):
    date_col, num_col = columns[0], columns[1]
    temp_df = df[[date_col, num_col]].dropna().sort_values(by=date_col)
    plt.figure(figsize=(10, 5))
    plt.plot(temp_df[date_col], temp_df[num_col])
    plt.title(f"{num_col} Over Time")
    plt.xlabel(date_col)
    plt.ylabel(num_col)
    plt.xticks(rotation=45)
    plt.grid(True)
    save_or_show_plot(output_folder, f"time_series_{clean_column_name(num_col)}_over_{clean_column_name(date_col)}.png")

def plot_bar_chart(df, columns, output_folder):
    cat_col = columns[0]
    counts = df[cat_col].value_counts().head(20)
    plt.figure(figsize=(10, 5))
    plt.bar(counts.index.astype(str), counts.values)
    plt.title(f"Category Count: {cat_col}")
    plt.xlabel(cat_col)
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    save_or_show_plot(output_folder, f"bar_count_{clean_column_name(cat_col)}.png")

def plot_pie_chart(df, columns, output_folder):
    cat_col = columns[0]
    counts = df[cat_col].value_counts().head(8)
    plt.figure(figsize=(8, 8))
    plt.pie(counts.values, labels=counts.index.astype(str), autopct="%1.1f%%")
    plt.title(f"Category Proportion: {cat_col}")
    save_or_show_plot(output_folder, f"pie_{clean_column_name(cat_col)}.png")

def plot_category_vs_numeric_bar(df, columns, output_folder):
    cat_col, num_col = columns[0], columns[1]
    grouped = df.groupby(cat_col)[num_col].mean().sort_values(ascending=False).head(20)
    plt.figure(figsize=(10, 5))
    plt.bar(grouped.index.astype(str), grouped.values)
    plt.title(f"Average {num_col} by {cat_col}")
    plt.xlabel(cat_col)
    plt.ylabel(f"Average {num_col}")
    plt.xticks(rotation=45)
    save_or_show_plot(output_folder, f"category_numeric_{clean_column_name(cat_col)}_{clean_column_name(num_col)}.png")

def plot_grouped_boxplot(df, columns, output_folder):
    cat_col, num_col = columns[0], columns[1]
    temp_df = df[[cat_col, num_col]].dropna()
    categories = temp_df[cat_col].value_counts().head(10).index
    data = [temp_df[temp_df[cat_col] == cat][num_col] for cat in categories]
    plt.figure(figsize=(10, 5))
    plt.boxplot(data, labels=[str(c) for c in categories])
    plt.title(f"{num_col} Distribution by {cat_col}")
    plt.xlabel(cat_col)
    plt.ylabel(num_col)
    plt.xticks(rotation=45)
    plt.grid(True)
    save_or_show_plot(output_folder, f"grouped_boxplot_{clean_column_name(cat_col)}_{clean_column_name(num_col)}.png")

def plot_boolean_bar(df, columns, output_folder):
    bool_col = columns[0]
    counts = df[bool_col].value_counts()
    plt.figure(figsize=(8, 5))
    plt.bar(counts.index.astype(str), counts.values)
    plt.title(f"Boolean Count: {bool_col}")
    plt.xlabel(bool_col)
    plt.ylabel("Count")
    plt.grid(True)
    save_or_show_plot(output_folder, f"boolean_bar_{clean_column_name(bool_col)}.png")

def plot_multi_line(df, columns, output_folder):
    plt.figure(figsize=(10, 5))
    for col in columns[:5]:
        plt.plot(df[col].reset_index(drop=True), label=col)
    plt.title("Multi-Line Plot")
    plt.xlabel("Row Index")
    plt.ylabel("Value")
    plt.legend()
    plt.grid(True)
    save_or_show_plot(output_folder, "multi_line_plot.png")

def plot_correlation_matrix(df, columns, output_folder):
    selected_df = df[columns].dropna()
    correlation = selected_df.corr()
    plt.figure(figsize=(8, 6))
    plt.imshow(correlation)
    plt.colorbar()
    plt.xticks(range(len(correlation.columns)), correlation.columns, rotation=45)
    plt.yticks(range(len(correlation.columns)), correlation.columns)
    plt.title("Correlation Matrix")
    for i in range(len(correlation.columns)):
        for j in range(len(correlation.columns)):
            plt.text(j, i, f"{correlation.iloc[i, j]:.2f}", ha="center", va="center")
    save_or_show_plot(output_folder, "correlation_matrix.png")

def generate_graph(df, suggestion, output_folder):
    gt = suggestion["graph_type"]
    cols = suggestion["columns"]
    if gt == "Histogram": plot_histogram(df, cols, output_folder)
    elif gt == "Box Plot": plot_boxplot(df, cols, output_folder)
    elif gt == "Scatter Plot": plot_scatter(df, cols, output_folder)
    elif gt == "Time Series Line Chart": plot_time_series(df, cols, output_folder)
    elif gt == "Bar Chart": plot_bar_chart(df, cols, output_folder)
    elif gt == "Pie Chart": plot_pie_chart(df, cols, output_folder)
    elif gt == "Category vs Numeric Bar Chart": plot_category_vs_numeric_bar(df, cols, output_folder)
    elif gt == "Grouped Box Plot": plot_grouped_boxplot(df, cols, output_folder)
    elif gt == "Boolean Bar Chart": plot_boolean_bar(df, cols, output_folder)
    elif gt == "Multi-Line Plot": plot_multi_line(df, cols, output_folder)
    elif gt == "Correlation Matrix": plot_correlation_matrix(df, cols, output_folder)
    else: print("No plotting function available for:", gt)



def create_output_folder(file_path):
    """
    Create output folder for graphs.
    """
    folder_name = "generated_graphs"
    if file_path:
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        folder_name = base_name + "_graphs"

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    return folder_name

def save_or_show_plot(output_folder, filename):
    """
    Save graph and show it.
    """
    full_path = os.path.join(output_folder, filename)
    plt.tight_layout()
    plt.savefig(full_path, dpi=150)
    print("Saved graph:", full_path)
    plt.show()


def automatic_graph(df,file_path):
    num_cols,cat_cols,date_cols,boolean_cols,text_cols,id_cols,location_cols=categorize_columns(df)
    suggestions = suggest_graphs(df, num_cols,cat_cols,date_cols,boolean_cols,text_cols,id_cols,location_cols)
    print(suggestions)
    output_folder = create_output_folder(file_path)
    
    if not suggestions:
        print("No Graph")
        return
    
    for suggestion in suggestions[:10]:
        print("Graph type :", suggestion["graph_type"],suggestion["columns"])
        generate_graph(df,suggestion,output_folder)
    print("saved graphs:",output_folder)
    
def column_names(df):
    cols = input("enter the column name :")
    
    
def main():
    print("STATISTICAL METHODS EXPLAINER")
    df = load_data()
    show_dataset(df)
    while True:
        menu()
        choice = input("\nEnter your choice: ").strip()
        if choice == "1":
             numeric_cols(df,num_cols)
        elif choice == "2":
            correlation(df,num_cols)
        elif choice == "3":
            linear_regression_demo(df)
        elif choice == "4":
            one_sample_t_test(df)
        elif choice == "5":
            independent_t_test(df)
        elif choice == "6":
            anova_demo(df)
        elif choice == "7":
            chi_square(df)
        elif choice == "8":
            run_all(df)
        elif choice == "0":
            print("\nExiting program.")
            break
        else:
            print("\nInvalid choice. Please try again.")
    automatic_graph(df,file_path)
main()
 
