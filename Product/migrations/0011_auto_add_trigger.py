from django.db import migrations

SQL = """
-- Create or replace the stored procedure
CREATE PROCEDURE update_product_avg_rating(IN product_id INT)
BEGIN
    DECLARE avg_rating DECIMAL(5, 2);
    SELECT AVG(LEAST(GREATEST(rate, 0.0), 5.0)) INTO avg_rating
    FROM rating
    WHERE product_id = product_id;

    UPDATE product
    SET rate = avg_rating
    WHERE id = product_id;
END;
"""

def create_trigger_and_procedure(apps, schema_editor):
    schema_editor.execute(SQL)

def remove_trigger_and_procedure(apps, schema_editor):
    # You may want to drop the trigger and procedure if needed
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0011_remove_product_rate_id_product_rate_and_more'),
    ]

    operations = [
        migrations.RunSQL(
            SQL,
            reverse_sql=remove_trigger_and_procedure  # Define reverse SQL if needed
        ),
    ]
