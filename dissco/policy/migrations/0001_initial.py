# Generated by Django 4.0.4 on 2022-05-30 23:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstitutionPolicyArea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.TextField(choices=[('documented', 'Documented'), ('undocumented', 'Undocumented'), ('not_in_place', 'Not In Place')])),
                ('documentation_date', models.DateTimeField(blank=True, null=True)),
                ('documentation_next_review_date', models.DateTimeField(blank=True, null=True)),
                ('documentation_public', models.TextField(blank=True)),
                ('documentation_shareable', models.TextField(blank=True)),
                ('documentation_provided', models.BooleanField(blank=True, null=True)),
                ('documentation_details', models.TextField()),
                ('policy_summary', models.TextField(blank=True)),
                ('additional_notes', models.TextField(blank=True)),
                ('institution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.institution')),
            ],
        ),
        migrations.CreateModel(
            name='PolicyArea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('number', models.IntegerField()),
                ('scope', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='PolicyCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('scope', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='PolicyComponent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('question', models.TextField()),
                ('description', models.TextField(blank=True)),
                ('type', models.TextField(choices=[('bool', 'Bool'), ('number', 'Number'), ('list', 'Option Single'), ('list+', 'Option Multiple')])),
                ('policy_area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='policy.policyarea')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceComponent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('description', models.TextField(blank=True)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='policy.service')),
            ],
        ),
        migrations.CreateModel(
            name='ServicePolicyMapping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('policy_component', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='policy.policycomponent')),
                ('service_component', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='policy.servicecomponent')),
            ],
        ),
        migrations.CreateModel(
            name='PolicyComponentOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField()),
                ('policy_component', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='policy.policycomponent')),
            ],
        ),
        migrations.AddField(
            model_name='policyarea',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='policy.policycategory'),
        ),
        migrations.CreateModel(
            name='InstitutionPolicyOwner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('role', models.TextField()),
                ('institution_policy_area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='policy.institutionpolicyarea')),
            ],
        ),
        migrations.CreateModel(
            name='InstitutionPolicyLanguage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.TextField(choices=[('ab', 'Abkhazian'), ('ae', 'Avestan'), ('af', 'Afrikaans'), ('ak', 'Akan'), ('am', 'Amharic'), ('an', 'Aragonese'), ('ar', 'Arabic'), ('as', 'Assamese'), ('av', 'Avaric'), ('ay', 'Aymara'), ('az', 'Azerbaijani'), ('ba', 'Bashkir'), ('be', 'Belarusian'), ('bg', 'Bulgarian'), ('bi', 'Bislama'), ('bm', 'Bambara'), ('bn', 'Bengali'), ('bo', 'Tibetan'), ('br', 'Breton'), ('bs', 'Bosnian'), ('ca', 'Catalan'), ('ce', 'Chechen'), ('ch', 'Chamorro'), ('co', 'Corsican'), ('cr', 'Cree'), ('cs', 'Czech'), ('cu', 'Church Slavic'), ('cv', 'Chuvash'), ('cy', 'Welsh'), ('da', 'Danish'), ('de', 'German'), ('dv', 'Dhivehi'), ('dz', 'Dzongkha'), ('el', 'Modern Greek (1453-)'), ('en', 'English'), ('eo', 'Esperanto'), ('es', 'Spanish'), ('et', 'Estonian'), ('eu', 'Basque'), ('fa', 'Persian'), ('fi', 'Finnish'), ('fj', 'Fijian'), ('fo', 'Faroese'), ('fr', 'French'), ('fy', 'Western Frisian'), ('ga', 'Irish'), ('gd', 'Scottish Gaelic'), ('gl', 'Galician'), ('gn', 'Guarani'), ('gu', 'Gujarati'), ('gv', 'Manx'), ('ha', 'Hausa'), ('he', 'Hebrew'), ('hi', 'Hindi'), ('ho', 'Hiri Motu'), ('hr', 'Croatian'), ('ht', 'Haitian'), ('hu', 'Hungarian'), ('hy', 'Armenian'), ('hz', 'Herero'), ('ia', 'Interlingua (International Auxiliary Language Association)'), ('id', 'Indonesian'), ('ie', 'Interlingue'), ('ig', 'Igbo'), ('ik', 'Inupiaq'), ('io', 'Ido'), ('is', 'Icelandic'), ('it', 'Italian'), ('iu', 'Inuktitut'), ('ja', 'Japanese'), ('jv', 'Javanese'), ('ka', 'Georgian'), ('kg', 'Kongo'), ('ki', 'Kikuyu'), ('kj', 'Kuanyama'), ('kl', 'Kalaallisut'), ('km', 'Central Khmer'), ('kn', 'Kannada'), ('ko', 'Korean'), ('kr', 'Kanuri'), ('ks', 'Kashmiri'), ('ku', 'Kurdish'), ('kv', 'Komi'), ('kw', 'Cornish'), ('ky', 'Kirghiz'), ('la', 'Latin'), ('lb', 'Luxembourgish'), ('lg', 'Ganda'), ('li', 'Limburgan'), ('ln', 'Lingala'), ('lo', 'Lao'), ('lt', 'Lithuanian'), ('lu', 'Luba-Katanga'), ('lv', 'Latvian'), ('mg', 'Malagasy'), ('mh', 'Marshallese'), ('mi', 'Maori'), ('mk', 'Macedonian'), ('ml', 'Malayalam'), ('mn', 'Mongolian'), ('mr', 'Marathi'), ('ms', 'Malay (macrolanguage)'), ('mt', 'Maltese'), ('my', 'Burmese'), ('na', 'Nauru'), ('nb', 'Norwegian Bokmål'), ('nd', 'North Ndebele'), ('ne', 'Nepali (macrolanguage)'), ('ng', 'Ndonga'), ('nl', 'Dutch'), ('no', 'Norwegian'), ('nr', 'South Ndebele'), ('nv', 'Navajo'), ('ny', 'Nyanja'), ('oc', 'Occitan (post 1500)'), ('oj', 'Ojibwa'), ('om', 'Oromo'), ('or', 'Oriya (macrolanguage)'), ('os', 'Ossetian'), ('pa', 'Panjabi'), ('pi', 'Pali'), ('pl', 'Polish'), ('ps', 'Pushto'), ('pt', 'Portuguese'), ('qu', 'Quechua'), ('rm', 'Romansh'), ('rn', 'Rundi'), ('ro', 'Romanian'), ('ru', 'Russian'), ('rw', 'Kinyarwanda'), ('sa', 'Sanskrit'), ('sc', 'Sardinian'), ('sd', 'Sindhi'), ('se', 'Northern Sami'), ('sg', 'Sango'), ('sh', 'Serbo-Croatian'), ('si', 'Sinhala'), ('sk', 'Slovak'), ('sl', 'Slovenian'), ('sm', 'Samoan'), ('sn', 'Shona'), ('so', 'Somali'), ('sq', 'Albanian'), ('sr', 'Serbian'), ('st', 'Southern Sotho'), ('su', 'Sundanese'), ('sv', 'Swedish'), ('sw', 'Swahili (macrolanguage)'), ('ta', 'Tamil'), ('te', 'Telugu'), ('tg', 'Tajik'), ('th', 'Thai'), ('ti', 'Tigrinya'), ('tk', 'Turkmen'), ('tl', 'Tagalog'), ('tn', 'Tswana'), ('to', 'Tonga (Tonga Islands)'), ('tr', 'Turkish'), ('ts', 'Tsonga'), ('tw', 'Twi'), ('ty', 'Tahitian'), ('ug', 'Uighur'), ('uk', 'Ukrainian'), ('ur', 'Urdu'), ('uz', 'Uzbek'), ('ve', 'Venda'), ('vi', 'Vietnamese'), ('vo', 'Volapük'), ('wa', 'Walloon'), ('wo', 'Wolof'), ('xh', 'Xhosa'), ('yi', 'Yiddish'), ('yo', 'Yoruba'), ('za', 'Zhuang'), ('zh', 'Chinese'), ('zu', 'Zulu')])),
                ('institution_policy_area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='policy.institutionpolicyarea')),
            ],
        ),
        migrations.CreateModel(
            name='InstitutionPolicyComponent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField(blank=True)),
                ('comment', models.TextField(blank=True)),
                ('chosen_options', models.ManyToManyField(to='policy.policycomponentoption')),
                ('institution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.institution')),
                ('policy_component', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='policy.policycomponent')),
            ],
        ),
        migrations.AddField(
            model_name='institutionpolicyarea',
            name='policy_area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='policy.policyarea'),
        ),
    ]
