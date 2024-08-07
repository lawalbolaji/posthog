# Generated by Django 4.2.14 on 2024-07-19 10:52

from django.db import migrations, models
import django.db.models.deletion


## Original Migration
# class Migration(migrations.Migration):
#     dependencies = [
#         ("posthog", "0444_integration_unique_id"),
#     ]

#     operations = [
#         migrations.AddField(
#             model_name="annotation",
#             name="dashboard",
#             field=models.ForeignKey(
#                 blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="posthog.dashboard"
#             ),
#         ),
#         migrations.AlterField(
#             model_name="annotation",
#             name="scope",
#             field=models.CharField(
#                 choices=[
#                     ("dashboard_item", "insight"),
#                     ("dashboard", "dashboard"),
#                     ("project", "project"),
#                     ("organization", "organization"),
#                 ],
#                 default="dashboard_item",
#                 max_length=24,
#             ),
#         ),
#     ]


class Migration(migrations.Migration):
    atomic = False  # Added to support concurrent index creation
    dependencies = [
        ("posthog", "0445_require_team_project_id_not_valid"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AddField(
                    model_name="annotation",
                    name="dashboard",
                    field=models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="posthog.dashboard",
                    ),
                )
            ],
            database_operations=[
                # We add -- existing-table-constraint-ignore to ignore the constraint validation in CI.
                migrations.RunSQL(
                    """
                    ALTER TABLE "posthog_annotation" ADD COLUMN "dashboard_id" integer NULL CONSTRAINT "posthog_annotation_dashboard_id_91ef4125_fk_posthog_d" REFERENCES "posthog_dashboard"("id") DEFERRABLE INITIALLY DEFERRED; -- existing-table-constraint-ignore
                    SET CONSTRAINTS "posthog_annotation_dashboard_id_91ef4125_fk_posthog_d" IMMEDIATE; -- existing-table-constraint-ignore
                    """,
                    reverse_sql="""
                        ALTER TABLE "posthog_annotation" DROP COLUMN IF EXISTS "dashboard_id";
                    """,
                ),
                # We add CONCURRENTLY to the create command
                migrations.RunSQL(
                    """
                    CREATE INDEX CONCURRENTLY "posthog_annotation_dashboard_id_91ef4125" ON "posthog_annotation" ("dashboard_id");
                    """,
                    reverse_sql="""
                        DROP INDEX IF EXISTS "posthog_annotation_dashboard_id_91ef4125";
                    """,
                ),
            ],
        ),
        migrations.AlterField(
            model_name="annotation",
            name="scope",
            field=models.CharField(
                choices=[
                    ("dashboard_item", "insight"),
                    ("dashboard", "dashboard"),
                    ("project", "project"),
                    ("organization", "organization"),
                ],
                default="dashboard_item",
                max_length=24,
            ),
        ),
    ]
