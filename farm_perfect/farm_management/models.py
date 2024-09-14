from django.contrib.gis.db import models

class Plot(models.Model):
    name = models.CharField(max_length=100)
    location = models.PolygonField()

    def __str__(self):
        return self.name

class Season(models.Model):
    plot = models.ForeignKey(Plot, on_delete=models.CASCADE, related_name='seasons')
    crop = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.crop} ({self.start_date} - {self.end_date})"

class SeasonalEvent(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='events')
    event_date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return f"{self.event_date}: {self.description}"
