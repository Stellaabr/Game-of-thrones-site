import matplotlib.pyplot as plt

def plot_deaths_by_year(df):
    deaths_year = df['Death Year'].value_counts().sort_index().dropna()

    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(deaths_year.index.astype(str), deaths_year.values,
                  color='#8B0000', edgecolor='black')

    if len(bars) <= 30:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2., height,
                    f'{int(height)}', ha='center', va='bottom')

    ax.set_title('Character Deaths by Year', fontsize=14, pad=20)
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Number of Deaths', fontsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.setp(ax.get_xticklabels(), rotation=45)
    fig.tight_layout()
    return fig

def plot_gender_nobility_death(df):
    dead_df = df[df['Death Year'].notna()].copy()

    pivot = dead_df.groupby(['Gender', 'Nobility']).size().unstack(fill_value=0)

    pivot.index = ['Female', 'Male']
    pivot.columns = ['Commoners', 'Nobility']

    fig, ax = plt.subplots(figsize=(10, 6))
    pivot.plot(kind='bar', stacked=True, ax=ax,
               color=['#FF9999', '#66B3FF'], edgecolor='black')

    ax.set_title('Mortality by Gender and Nobility', fontsize=14, pad=20)
    ax.set_xlabel('Gender', fontsize=12)
    ax.set_ylabel('Number of Deaths', fontsize=12)
    ax.tick_params(axis='x', rotation=0)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    ax.legend(title='Social Status')
    fig.tight_layout()
    return fig

def plot_top_allegiances(df, n=10):
    top_houses = df['Allegiances'].value_counts().nlargest(n)

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.barh(top_houses.index, top_houses.values, color='#4682B4', edgecolor='black')
    ax.set_title(f'Top-{n} Houses by Deaths', fontsize=14, pad=20)
    ax.set_xlabel('Number of Deaths', fontsize=12)
    ax.set_ylabel('House/Organization', fontsize=12)
    ax.invert_yaxis()
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    fig.tight_layout()
    return fig

def plot_deaths_by_book_pie(df):
    book_names = ['GoT', 'CoK', 'SoS', 'FfC', 'DwD']
    deaths = df['Book of Death'].value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(10, 7))
    ax.pie(deaths, labels=book_names, autopct='%1.1f%%', startangle=90,
           colors=['#FF9999', '#66B3FF', '#99FF99', '#FFCC99', '#C2C2F0'])
    ax.set_title('Death Distribution by Book', fontsize=14, pad=20)
    fig.tight_layout()
    return fig