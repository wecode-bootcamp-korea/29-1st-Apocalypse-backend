# Generated by Django 4.0.1 on 2022-01-25 10:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcomponent',
            name='component',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productcomponent_components', to='products.component'),
        ),
        migrations.AlterField(
            model_name='productcomponent',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productcomponent_products', to='products.product'),
        ),
        migrations.AlterField(
            model_name='productpreference',
            name='preference',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productpreference_preferencess', to='products.preference'),
        ),
        migrations.AlterField(
            model_name='productpreference',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productpreference_products', to='products.product'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_categories', to='products.category'),
        ),
    ]
