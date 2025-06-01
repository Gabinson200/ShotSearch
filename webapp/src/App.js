import React, { useState } from 'react';
import {
  Container,
  Paper,
  Typography,
  TextField,
  Button,
  Box,
  Grid,
  Chip,
  CircularProgress,
  Card,
  CardContent,
  CardHeader,
  CardActions,
  Avatar,
} from '@mui/material';
import { ThemeProvider } from '@mui/material/styles';
import { theme } from './theme';
import axios from 'axios';
import TravelExploreIcon from '@mui/icons-material/TravelExplore';
import VaccinesIcon from '@mui/icons-material/Vaccines';
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';
import PersonIcon from '@mui/icons-material/Person';
import InfoIcon from '@mui/icons-material/Info';

function App() {
  const [formData, setFormData] = useState({
    destinationCountry: '',
    age: '',
    vaccinationHistory: [],
    specificQuestions: [],
    travelDate: '',
  });

  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleAddVaccination = () => {
    setFormData({
      ...formData,
      vaccinationHistory: [...formData.vaccinationHistory, ''],
    });
  };

  const handleAddQuestion = () => {
    setFormData({
      ...formData,
      specificQuestions: [...formData.specificQuestions, ''],
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/vaccination-info', {
        destination_country: formData.destinationCountry,
        age: parseInt(formData.age),
        vaccination_history: formData.vaccinationHistory,
        specific_questions: formData.specificQuestions,
        travel_date: formData.travelDate,
      });
      setResults(response.data);
    } catch (error) {
      console.error('Error:', error);
      alert('Error fetching vaccination information. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <Container maxWidth="md" sx={{ mt: 4, bgcolor: 'background.default' }}>
        <Paper elevation={3} sx={{
          p: 4,
          bgcolor: 'background.paper',
          borderRadius: 2,
          boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
        }}>
          <Box sx={{ mb: 4 }}>
            <Typography variant="h4" component="h1" gutterBottom>
              Travel Vaccination Guide
            </Typography>
            <Typography variant="subtitle1" color="text.secondary" paragraph>
              Get personalized vaccination recommendations for your destination
            </Typography>
          </Box>

        <form onSubmit={handleSubmit}>
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <Card>
                <CardHeader
                  avatar={
                    <Avatar sx={{ bgcolor: 'primary.main' }}>
                      <TravelExploreIcon />
                    </Avatar>
                  }
                  title="Destination Details"
                />
                <CardContent>
                  <TextField
                    fullWidth
                    label="Destination Country"
                    name="destinationCountry"
                    value={formData.destinationCountry}
                    onChange={handleChange}
                    required
                  />
                  <TextField
                    fullWidth
                    label="Travel Date"
                    name="travelDate"
                    value={formData.travelDate}
                    onChange={handleChange}
                    type="date"
                    required
                    InputLabelProps={{
                      shrink: true,
                    }}
                    sx={{ mt: 2 }}
                  />
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12}>
              <Card>
                <CardHeader
                  avatar={
                    <Avatar sx={{ bgcolor: 'secondary.main' }}>
                      <PersonIcon />
                    </Avatar>
                  }
                  title="Personal Information"
                />
                <CardContent>
                  <TextField
                    fullWidth
                    label="Age"
                    name="age"
                    value={formData.age}
                    onChange={handleChange}
                    type="number"
                    required
                  />
                </CardContent>
              </Card>
            </Grid>
          </Grid>



          <Card sx={{ mb: 2 }}>
            <CardHeader
              avatar={
                <Avatar sx={{ bgcolor: 'primary.main' }}>
                  <VaccinesIcon />
                </Avatar>
              }
              title="Vaccination History"
            />
            <CardContent>
              {formData.vaccinationHistory.map((_, index) => (
                <TextField
                  key={index}
                  fullWidth
                  label={`Vaccination ${index + 1}`}
                  value={formData.vaccinationHistory[index]}
                  onChange={(e) => {
                    const newHistory = [...formData.vaccinationHistory];
                    newHistory[index] = e.target.value;
                    setFormData({ ...formData, vaccinationHistory: newHistory });
                  }}
                  margin="normal"
                />
              ))}
              <Button
                variant="outlined"
                onClick={handleAddVaccination}
                startIcon={<VaccinesIcon />}
                sx={{ mt: 1, width: 'fit-content' }}
              >
                Add Vaccination
              </Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader
              avatar={
                <Avatar sx={{ bgcolor: 'secondary.main' }}>
                  <HelpOutlineIcon />
                </Avatar>
              }
              title="Specific Questions"
            />
            <CardContent>
              {formData.specificQuestions.map((_, index) => (
                <TextField
                  key={index}
                  fullWidth
                  label={`Question ${index + 1}`}
                  value={formData.specificQuestions[index]}
                  onChange={(e) => {
                    const newQuestions = [...formData.specificQuestions];
                    newQuestions[index] = e.target.value;
                    setFormData({ ...formData, specificQuestions: newQuestions });
                  }}
                  margin="normal"
                />
              ))}
              <Button
                variant="outlined"
                onClick={handleAddQuestion}
                startIcon={<HelpOutlineIcon />}
                sx={{ mt: 1, width: 'fit-content' }}
              >
                Add Question
              </Button>
            </CardContent>
          </Card>

          <CardActions sx={{ justifyContent: 'center', mt: 2 }}>
            <Button
              type="submit"
              variant="contained"
              size="large"
              sx={{
                px: 4,
                bgcolor: 'primary.main',
                '&:hover': {
                  bgcolor: 'primary.dark',
                },
              }}
              disabled={loading}
            >
              {loading ? (
                <>
                  <CircularProgress size={24} sx={{ color: 'white', mr: 1 }} />
                  Processing...
                </>
              ) : (
                <>
                  <InfoIcon sx={{ mr: 1 }} />
                  Get Vaccination Info
                </>
              )}
            </Button>
          </CardActions>
        </form>

        {results && (
          <Paper sx={{ mt: 4, p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Vaccination Information
            </Typography>
            <Typography variant="h6" gutterBottom>
              Vaccination Information
            </Typography>
            
            {results.required_vaccinations.length > 0 && (
              <>
                <Typography variant="subtitle1" gutterBottom>
                  Required Vaccinations:
                </Typography>
                {results.required_vaccinations.map((vacc, index) => (
                  <Chip
                    key={index}
                    label={vacc}
                    color="primary"
                    sx={{
                      my: 1,
                      bgcolor: 'primary.light',
                      color: 'primary.contrastText',
                    }}
                  />
                ))}
              </>
            )}

            {results.recommended_vaccinations.length > 0 && (
              <>
                <Typography variant="subtitle1" gutterBottom>
                  Recommended Vaccinations:
                </Typography>
                {results.recommended_vaccinations.map((vacc, index) => (
                  <Chip
                    key={index}
                    label={vacc}
                    color="secondary"
                    sx={{
                      my: 1,
                      bgcolor: 'secondary.light',
                      color: 'secondary.contrastText',
                    }}
                  />
                ))}
              </>
            )}

            {results.specific_advice.length > 0 && (
              <>
                <Typography variant="subtitle1" gutterBottom>
                  Specific Advice:
                </Typography>
                {results.specific_advice.map((advice, index) => (
                  <Typography
                    key={index}
                    variant="body1"
                    sx={{
                      color: 'text.secondary',
                      mb: 1,
                      '&:before': {
                        content: '"•"',
                        color: 'primary.main',
                        display: 'inline-block',
                        width: '1em',
                        margin: '0 0.5em 0 -1em',
                      },
                    }}
                  >
                    {advice}
                  </Typography>
                ))}
              </>
            )}

            {results.additional_notes.length > 0 && (
              <>
                <Typography variant="subtitle1" gutterBottom>
                  Additional Notes:
                </Typography>
                {results.additional_notes.map((note, index) => (
                  <Typography
                    key={index}
                    variant="body1"
                    sx={{
                      color: 'text.secondary',
                      mb: 1,
                      '&:before': {
                        content: '"•"',
                        color: 'secondary.main',
                        display: 'inline-block',
                        width: '1em',
                        margin: '0 0.5em 0 -1em',
                      },
                    }}
                  >
                    {note}
                  </Typography>
                ))}
              </>
            )}
          </Paper>
        )}
        </Paper>
      </Container>
    </ThemeProvider>
  );
}

export default App;
